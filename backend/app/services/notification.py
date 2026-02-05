"""Email notification service using Resend."""
import os
import asyncio
import logging
import resend
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from ..models.notification import NotificationPreference, NotificationLog
from ..models.project import Project
from ..models.user import User

logger = logging.getLogger(__name__)

# Initialize Resend
resend.api_key = os.environ.get('RESEND_API_KEY', '')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'notifications@hhdrywall.pro')


class NotificationService:
    """Service for managing and sending email notifications."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_preferences(self, user_id: int) -> Optional[NotificationPreference]:
        """Get notification preferences for a user."""
        return self.db.query(NotificationPreference).filter(
            NotificationPreference.user_id == user_id
        ).first()
    
    def create_or_update_preferences(
        self,
        user_id: int,
        email_enabled: bool = True,
        frequency: str = 'daily',
        min_project_value: float = 1000000,
        preferred_sectors: List[str] = None,
        preferred_regions: List[str] = None,
        match_type: str = 'any'
    ) -> NotificationPreference:
        """Create or update notification preferences."""
        prefs = self.get_user_preferences(user_id)
        
        if prefs:
            prefs.email_enabled = email_enabled
            prefs.frequency = frequency
            prefs.min_project_value = min_project_value
            prefs.preferred_sectors = preferred_sectors or []
            prefs.preferred_regions = preferred_regions or []
            prefs.match_type = match_type
            prefs.updated_at = datetime.utcnow()
        else:
            prefs = NotificationPreference(
                user_id=user_id,
                email_enabled=email_enabled,
                frequency=frequency,
                min_project_value=min_project_value,
                preferred_sectors=preferred_sectors or [],
                preferred_regions=preferred_regions or [],
                match_type=match_type
            )
            self.db.add(prefs)
        
        self.db.commit()
        self.db.refresh(prefs)
        return prefs
    
    def check_project_matches(
        self,
        project: Project,
        prefs: NotificationPreference
    ) -> bool:
        """Check if a project matches user preferences."""
        matches = []
        
        # Check value threshold
        if project.value and project.value >= prefs.min_project_value:
            matches.append(True)
        else:
            matches.append(False)
        
        # Check sector match
        if prefs.preferred_sectors:
            sector_match = project.sector in prefs.preferred_sectors if project.sector else False
            matches.append(sector_match)
        
        # Check region match
        if prefs.preferred_regions:
            region_match = project.state in prefs.preferred_regions if project.state else False
            matches.append(region_match)
        
        # Apply match type logic
        if prefs.match_type == 'all':
            return all(matches) if matches else False
        else:  # 'any'
            return any(matches) if matches else False
    
    def get_matching_projects(
        self,
        user: User,
        prefs: NotificationPreference,
        since: Optional[datetime] = None
    ) -> List[Project]:
        """Get projects matching user preferences."""
        query = self.db.query(Project).filter(Project.tenant_id == user.tenant_id)
        
        if since:
            query = query.filter(Project.created_at >= since)
        
        projects = query.all()
        
        matching = [p for p in projects if self.check_project_matches(p, prefs)]
        return matching
    
    def build_email_html(
        self,
        user: User,
        projects: List[Project],
        notification_type: str
    ) -> str:
        """Build HTML email content."""
        project_rows = ""
        for p in projects[:10]:  # Limit to 10 projects
            value_str = f"${p.value/1000000:.1f}M" if p.value else "N/A"
            project_rows += f"""
            <tr>
                <td style="padding: 12px; border-bottom: 1px solid #334155;">
                    <strong style="color: #fff;">{p.title}</strong><br>
                    <span style="color: #94a3b8; font-size: 14px;">{p.sector or 'N/A'} • {p.city or ''}, {p.state or ''}</span>
                </td>
                <td style="padding: 12px; border-bottom: 1px solid #334155; text-align: right;">
                    <span style="color: #10b981; font-size: 18px; font-weight: bold;">{value_str}</span><br>
                    <span style="color: #94a3b8; font-size: 12px;">{p.status or 'Active'}</span>
                </td>
            </tr>
            """
        
        title = "New Project Alert" if notification_type == 'realtime' else "Your Daily Project Digest"
        subtitle = "A project matching your preferences was just added" if notification_type == 'realtime' else f"Here are {len(projects)} projects matching your preferences"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; background-color: #0f172a; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <tr>
                    <td style="padding: 20px; background-color: #1e293b; border-radius: 12px;">
                        <!-- Header -->
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td style="padding-bottom: 20px; border-bottom: 1px solid #334155;">
                                    <h1 style="margin: 0; color: #3b82f6; font-size: 24px;">HHDrywall Pro</h1>
                                    <p style="margin: 5px 0 0 0; color: #94a3b8; font-size: 14px;">Construction Market Intelligence</p>
                                </td>
                            </tr>
                        </table>
                        
                        <!-- Title -->
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td style="padding: 20px 0;">
                                    <h2 style="margin: 0; color: #fff; font-size: 20px;">{title}</h2>
                                    <p style="margin: 5px 0 0 0; color: #94a3b8;">{subtitle}</p>
                                </td>
                            </tr>
                        </table>
                        
                        <!-- Projects Table -->
                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #0f172a; border-radius: 8px;">
                            {project_rows}
                        </table>
                        
                        <!-- CTA Button -->
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td style="padding: 20px 0; text-align: center;">
                                    <a href="#" style="display: inline-block; padding: 12px 24px; background-color: #3b82f6; color: #fff; text-decoration: none; border-radius: 8px; font-weight: bold;">
                                        View All Projects
                                    </a>
                                </td>
                            </tr>
                        </table>
                        
                        <!-- Footer -->
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td style="padding-top: 20px; border-top: 1px solid #334155; text-align: center;">
                                    <p style="margin: 0; color: #64748b; font-size: 12px;">
                                        You're receiving this because you enabled project notifications.<br>
                                        <a href="#" style="color: #3b82f6;">Manage preferences</a> | <a href="#" style="color: #3b82f6;">Unsubscribe</a>
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        return html
    
    async def send_notification(
        self,
        user: User,
        projects: List[Project],
        notification_type: str = 'realtime'
    ) -> Dict[str, Any]:
        """Send email notification to user."""
        if not projects:
            return {"status": "skipped", "reason": "No matching projects"}
        
        # Build email
        subject = f"🏗️ {len(projects)} New Project{'s' if len(projects) > 1 else ''} Matching Your Preferences"
        if notification_type == 'daily':
            subject = f"📊 Your Daily Project Digest - {len(projects)} Opportunities"
        
        html_content = self.build_email_html(user, projects, notification_type)
        
        # Create log entry
        log = NotificationLog(
            user_id=user.id,
            notification_type=notification_type,
            subject=subject,
            recipient_email=user.email,
            project_ids=[p.id for p in projects],
            status='pending'
        )
        self.db.add(log)
        self.db.commit()
        
        try:
            params = {
                "from": SENDER_EMAIL,
                "to": [user.email],
                "subject": subject,
                "html": html_content
            }
            
            # Run sync SDK in thread to keep non-blocking
            email = await asyncio.to_thread(resend.Emails.send, params)
            
            # Update log
            log.status = 'sent'
            log.sent_at = datetime.utcnow()
            self.db.commit()
            
            # Update last notified timestamp
            prefs = self.get_user_preferences(user.id)
            if prefs:
                prefs.last_notified_at = datetime.utcnow()
                self.db.commit()
            
            logger.info(f"Notification sent to {user.email}")
            return {
                "status": "success",
                "email_id": email.get("id"),
                "recipient": user.email,
                "projects_count": len(projects)
            }
            
        except Exception as e:
            log.status = 'failed'
            log.error_message = str(e)[:500]
            self.db.commit()
            
            logger.error(f"Failed to send notification to {user.email}: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    async def process_daily_digests(self) -> List[Dict]:
        """Process and send daily digest notifications."""
        results = []
        
        # Get all users with daily notifications enabled
        prefs_list = self.db.query(NotificationPreference).filter(
            NotificationPreference.email_enabled == True,
            NotificationPreference.frequency == 'daily'
        ).all()
        
        for prefs in prefs_list:
            user = self.db.query(User).filter(User.id == prefs.user_id).first()
            if not user:
                continue
            
            # Get projects from last 24 hours
            since = datetime.utcnow() - timedelta(hours=24)
            matching_projects = self.get_matching_projects(user, prefs, since)
            
            if matching_projects:
                result = await self.send_notification(user, matching_projects, 'daily')
                results.append({
                    "user_id": user.id,
                    "email": user.email,
                    **result
                })
        
        return results
