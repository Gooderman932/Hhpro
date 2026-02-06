"""AI-powered data enrichment service."""
import os
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session


class AIEnrichmentService:
    """AI service for enriching project data and generating insights."""
    
    # Trade classifications
    TRADE_CATEGORIES = {
        "electrical": ["electrical", "wiring", "power", "lighting", "panel", "conduit"],
        "plumbing": ["plumbing", "pipe", "water", "drain", "sewer", "fixture"],
        "hvac": ["hvac", "heating", "cooling", "ventilation", "air conditioning", "ductwork"],
        "drywall": ["drywall", "sheetrock", "gypsum", "wall board", "partition"],
        "roofing": ["roof", "roofing", "shingle", "membrane", "flashing"],
        "concrete": ["concrete", "foundation", "slab", "cement", "masonry"],
        "structural": ["steel", "framing", "structural", "beam", "column"],
        "flooring": ["floor", "tile", "carpet", "hardwood", "epoxy"],
        "painting": ["paint", "coating", "finish", "primer"],
        "landscaping": ["landscape", "irrigation", "hardscape", "grading"],
    }
    
    SECTOR_KEYWORDS = {
        "Healthcare": ["hospital", "medical", "clinic", "healthcare", "patient", "surgical"],
        "Education": ["school", "university", "college", "classroom", "education", "campus"],
        "Retail": ["retail", "store", "shop", "mall", "commercial", "tenant"],
        "Office": ["office", "corporate", "business", "workspace", "commercial"],
        "Industrial": ["warehouse", "manufacturing", "industrial", "factory", "distribution"],
        "Hospitality": ["hotel", "restaurant", "hospitality", "lodging", "resort"],
        "Residential": ["residential", "apartment", "condo", "housing", "multifamily", "home"],
        "Infrastructure": ["road", "bridge", "utility", "infrastructure", "municipal"],
    }
    
    def __init__(self, use_llm: bool = True):
        self.use_llm = use_llm
        self.llm_available = self._check_llm_availability()
    
    def _check_llm_availability(self) -> bool:
        """Check if LLM API is available."""
        api_key = os.environ.get("EMERGENT_API_KEY") or os.environ.get("OPENAI_API_KEY")
        return bool(api_key)
    
    def categorize_by_trade(self, text: str) -> List[str]:
        """Categorize project by trade based on text analysis."""
        text_lower = text.lower()
        matched_trades = []
        
        for trade, keywords in self.TRADE_CATEGORIES.items():
            if any(kw in text_lower for kw in keywords):
                matched_trades.append(trade)
        
        return matched_trades if matched_trades else ["general"]
    
    def categorize_by_sector(self, text: str) -> str:
        """Categorize project by sector."""
        text_lower = text.lower()
        
        for sector, keywords in self.SECTOR_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                return sector
        
        return "Commercial"
    
    def estimate_project_complexity(self, value: float, description: str) -> str:
        """Estimate project complexity based on value and description."""
        if value > 10000000:
            return "high"
        elif value > 2000000:
            return "medium"
        else:
            return "low"
    
    def generate_project_insights(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI insights for a project."""
        name = project.get("name", "")
        description = project.get("description", "")
        value = project.get("value", 0)
        sector = project.get("sector", "")
        
        combined_text = f"{name} {description} {sector}"
        
        # Rule-based analysis
        trades = self.categorize_by_trade(combined_text)
        detected_sector = self.categorize_by_sector(combined_text)
        complexity = self.estimate_project_complexity(value, combined_text)
        
        # Generate insights
        insights = []
        
        if value > 5000000:
            insights.append("High-value project - consider forming joint venture or partnership")
        
        if "healthcare" in detected_sector.lower():
            insights.append("Healthcare projects typically require specialized certifications")
        
        if "renovation" in combined_text.lower():
            insights.append("Renovation project - assess existing conditions carefully")
        
        if complexity == "high":
            insights.append("Complex project - allocate additional project management resources")
        
        return {
            "detected_trades": trades,
            "detected_sector": detected_sector,
            "complexity": complexity,
            "insights": insights,
            "match_score": self._calculate_match_score(project),
            "enriched": True
        }
    
    def _calculate_match_score(self, project: Dict[str, Any]) -> int:
        """Calculate how well a project matches typical criteria."""
        score = 50  # Base score
        
        value = project.get("value", 0)
        if 500000 <= value <= 10000000:
            score += 20  # Sweet spot for most contractors
        elif value > 10000000:
            score += 10
        
        if project.get("sector"):
            score += 10
        
        if project.get("description"):
            score += 10
        
        return min(score, 100)
    
    def match_projects_to_profile(
        self, 
        projects: List[Dict[str, Any]], 
        user_profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Match and rank projects based on user profile."""
        user_trades = user_profile.get("trade_specialty", "").lower()
        user_sectors = user_profile.get("preferred_sectors", [])
        user_states = user_profile.get("service_states", [])
        min_value = user_profile.get("min_project_value", 0)
        max_value = user_profile.get("max_project_value", float("inf"))
        
        scored_projects = []
        
        for project in projects:
            score = 0
            reasons = []
            
            # Location match
            if project.get("state") in user_states:
                score += 30
                reasons.append("In your service area")
            
            # Value match
            value = project.get("value", 0) or project.get("estimated_value", 0)
            if min_value <= value <= max_value:
                score += 25
                reasons.append("Within your value range")
            
            # Sector match
            project_sector = project.get("sector", "")
            if project_sector in user_sectors:
                score += 25
                reasons.append(f"Matches preferred sector: {project_sector}")
            
            # Trade match
            project_text = f"{project.get('name', '')} {project.get('description', '')}"
            if user_trades and user_trades in project_text.lower():
                score += 20
                reasons.append(f"Matches your trade: {user_trades}")
            
            scored_projects.append({
                **project,
                "match_score": score,
                "match_reasons": reasons
            })
        
        # Sort by match score
        scored_projects.sort(key=lambda x: x["match_score"], reverse=True)
        
        return scored_projects
    
    async def enrich_with_llm(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Use LLM for advanced enrichment (if available)."""
        if not self.llm_available:
            return self.generate_project_insights(project)
        
        try:
            from emergentintegrations.llm.openai import OpenAI, ChatRequest
            
            api_key = os.environ.get("EMERGENT_API_KEY")
            if not api_key:
                return self.generate_project_insights(project)
            
            client = OpenAI(api_key=api_key)
            
            prompt = f"""Analyze this construction project and provide insights:

Project Name: {project.get('name', 'N/A')}
Description: {project.get('description', 'N/A')}
Value: ${project.get('value', 0):,.0f}
Location: {project.get('city', '')}, {project.get('state', '')}
Sector: {project.get('sector', 'N/A')}

Provide:
1. Key trades likely needed
2. Potential challenges
3. Timeline estimate
4. Competition level (low/medium/high)

Be concise - 2-3 sentences per point."""

            response = await client.chat(ChatRequest(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            ))
            
            base_insights = self.generate_project_insights(project)
            base_insights["llm_analysis"] = response.content
            
            return base_insights
            
        except Exception as e:
            print(f"LLM enrichment error: {e}")
            return self.generate_project_insights(project)
