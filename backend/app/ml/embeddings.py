"""
Embeddings and Similarity Service
Vector embeddings for semantic search and project similarity matching
"""
import numpy as np
from typing import List, Dict, Optional, Tuple
import openai
from sklearn.metrics.pairwise import cosine_similarity
from loguru import logger
from sqlalchemy.orm import Session
import json

from app.config import settings
from app.models.project import Project


class EmbeddingsService:
    """
    Generate and manage vector embeddings for semantic search
    """
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.embedding_model = settings.OPENAI_EMBEDDING_MODEL
        self.embedding_dimension = 1536  # For text-embedding-3-small
        
    def generate_project_embedding(self, project: Project) -> np.ndarray:
        """
        Generate semantic embedding for a project
        Combines title, description, and metadata
        """
        # Construct text representation
        text_parts = [project.title]
        
        if project.description:
            text_parts.append(project.description[:1000])  # Limit description length
        
        # Add metadata for richer representation
        if project.project_type:
            text_parts.append(f"Type: {project.project_type.value}")
        
        if project.region and project.country:
            text_parts.append(f"Location: {project.region}, {project.country}")
        
        if project.estimated_value:
            value_str = f"${project.estimated_value:,.0f}"
            text_parts.append(f"Value: {value_str}")
        
        text = " | ".join(text_parts)
        
        # Generate embedding using OpenAI
        try:
            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            
            embedding = np.array(response.data[0].embedding)
            return embedding
            
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            return None
    
    def generate_text_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for arbitrary text (search queries, etc.)"""
        try:
            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=text[:8000]  # API limit
            )
            
            return np.array(response.data[0].embedding)
            
        except Exception as e:
            logger.error(f"Failed to generate text embedding: {e}")
            return None
    
    def find_similar_projects(self,
                            query_project: Project,
                            db: Session,
                            top_k: int = 10,
                            min_similarity: float = 0.7) -> List[Dict]:
        """
        Find projects similar to the query project
        
        Args:
            query_project: Project to find similar matches for
            top_k: Number of results to return
            min_similarity: Minimum cosine similarity threshold
            
        Returns:
            List of similar projects with similarity scores
        """
        # Generate embedding for query project if not already done
        if not query_project.embeddings:
            query_embedding = self.generate_project_embedding(query_project)
            if query_embedding is None:
                return []
        else:
            query_embedding = np.array(json.loads(query_project.embeddings))
        
        # Get all projects with embeddings in same tenant
        candidate_projects = db.query(Project).filter(
            Project.tenant_id == query_project.tenant_id,
            Project.id != query_project.id,
            Project.embeddings.isnot(None)
        ).all()
        
        if not candidate_projects:
            logger.warning("No projects with embeddings found for similarity search")
            return []
        
        # Calculate similarities
        similarities = []
        for candidate in candidate_projects:
            candidate_embedding = np.array(json.loads(candidate.embeddings))
            
            similarity = cosine_similarity(
                query_embedding.reshape(1, -1),
                candidate_embedding.reshape(1, -1)
            )[0][0]
            
            if similarity >= min_similarity:
                similarities.append({
                    'project': candidate,
                    'similarity': float(similarity)
                })
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        results = []
        for item in similarities[:top_k]:
            results.append({
                'project_id': item['project'].id,
                'title': item['project'].title,
                'project_type': item['project'].project_type.value if item['project'].project_type else None,
                'region': item['project'].region,
                'estimated_value': item['project'].estimated_value,
                'similarity_score': item['similarity'],
                'match_reason': self._explain_similarity(query_project, item['project'], item['similarity'])
            })
        
        return results
    
    def semantic_search(self,
                       query_text: str,
                       db: Session,
                       tenant_id: int,
                       filters: Optional[Dict] = None,
                       top_k: int = 20) -> List[Dict]:
        """
        Semantic search across projects using natural language query
        
        Example queries:
        - "data centers in Texas worth more than $50M"
        - "hospital projects starting in 2025"
        - "commercial construction in the midwest"
        """
        # Generate query embedding
        query_embedding = self.generate_text_embedding(query_text)
        if query_embedding is None:
            return []
        
        # Get candidate projects
        query_obj = db.query(Project).filter(
            Project.tenant_id == tenant_id,
            Project.embeddings.isnot(None)
        )
        
        # Apply filters if provided
        if filters:
            if 'project_type' in filters:
                query_obj = query_obj.filter(Project.project_type == filters['project_type'])
            if 'country' in filters:
                query_obj = query_obj.filter(Project.country == filters['country'])
            if 'region' in filters:
                query_obj = query_obj.filter(Project.region == filters['region'])
            if 'min_value' in filters:
                query_obj = query_obj.filter(Project.estimated_value >= filters['min_value'])
            if 'max_value' in filters:
                query_obj = query_obj.filter(Project.estimated_value <= filters['max_value'])
        
        candidates = query_obj.all()
        
        if not candidates:
            return []
        
        # Calculate similarities
        results = []
        for project in candidates:
            project_embedding = np.array(json.loads(project.embeddings))
            
            similarity = cosine_similarity(
                query_embedding.reshape(1, -1),
                project_embedding.reshape(1, -1)
            )[0][0]
            
            results.append({
                'project_id': project.id,
                'title': project.title,
                'description': project.description[:200] if project.description else None,
                'project_type': project.project_type.value if project.project_type else None,
                'region': project.region,
                'country': project.country,
                'estimated_value': project.estimated_value,
                'stage': project.stage.value if project.stage else None,
                'relevance_score': float(similarity)
            })
        
        # Sort by relevance
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return results[:top_k]
    
    def find_similar_companies_by_projects(self,
                                          company_id: int,
                                          db: Session,
                                          top_k: int = 10) -> List[Dict]:
        """
        Find companies with similar project portfolios
        Useful for competitive intelligence
        """
        from app.models.project import ProjectParticipant
        from app.models.company import Company
        
        # Get projects this company worked on
        company_projects = db.query(Project).join(ProjectParticipant).filter(
            ProjectParticipant.company_id == company_id,
            Project.embeddings.isnot(None)
        ).all()
        
        if not company_projects:
            return []
        
        # Calculate average embedding for company's portfolio
        company_embeddings = [
            np.array(json.loads(p.embeddings)) 
            for p in company_projects
        ]
        company_avg_embedding = np.mean(company_embeddings, axis=0)
        
        # Get other companies and their portfolios
        other_companies = db.query(Company).filter(
            Company.id != company_id,
            Company.tenant_id == db.query(Company).filter(Company.id == company_id).first().tenant_id
        ).all()
        
        similarities = []
        for other_company in other_companies:
            # Get their projects
            other_projects = db.query(Project).join(ProjectParticipant).filter(
                ProjectParticipant.company_id == other_company.id,
                Project.embeddings.isnot(None)
            ).all()
            
            if not other_projects:
                continue
            
            # Calculate their average embedding
            other_embeddings = [
                np.array(json.loads(p.embeddings))
                for p in other_projects
            ]
            other_avg_embedding = np.mean(other_embeddings, axis=0)
            
            # Calculate similarity
            similarity = cosine_similarity(
                company_avg_embedding.reshape(1, -1),
                other_avg_embedding.reshape(1, -1)
            )[0][0]
            
            similarities.append({
                'company_id': other_company.id,
                'company_name': other_company.name,
                'company_type': other_company.company_type.value if other_company.company_type else None,
                'similarity': float(similarity),
                'shared_project_types': self._find_shared_project_types(company_projects, other_projects)
            })
        
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        return similarities[:top_k]
    
    def _explain_similarity(self, project1: Project, project2: Project, score: float) -> str:
        """Generate human-readable explanation of similarity"""
        reasons = []
        
        # Type match
        if project1.project_type == project2.project_type:
            reasons.append(f"Same type ({project1.project_type.value})")
        
        # Geographic proximity
        if project1.region == project2.region:
            reasons.append(f"Same region ({project1.region})")
        elif project1.country == project2.country:
            reasons.append(f"Same country ({project1.country})")
        
        # Size similarity
        if project1.estimated_value and project2.estimated_value:
            ratio = project1.estimated_value / project2.estimated_value
            if 0.5 <= ratio <= 2.0:
                reasons.append("Similar size")
        
        # Stage
        if project1.stage == project2.stage:
            reasons.append(f"Same stage ({project1.stage.value})")
        
        if not reasons:
            reasons.append("Semantic content similarity")
        
        return ", ".join(reasons)
    
    def _find_shared_project_types(self, projects1: List[Project], projects2: List[Project]) -> List[str]:
        """Find common project types between two portfolios"""
        types1 = set(p.project_type.value for p in projects1 if p.project_type)
        types2 = set(p.project_type.value for p in projects2 if p.project_type)
        
        return list(types1 & types2)
    
    def batch_generate_embeddings(self,
                                 projects: List[Project],
                                 db: Session,
                                 update_db: bool = True) -> Dict:
        """
        Generate embeddings for multiple projects efficiently
        Use for bulk processing / backfilling
        """
        logger.info(f"Generating embeddings for {len(projects)} projects")
        
        success_count = 0
        error_count = 0
        
        for i, project in enumerate(projects):
            if i % 50 == 0:
                logger.info(f"Progress: {i}/{len(projects)}")
            
            try:
                embedding = self.generate_project_embedding(project)
                
                if embedding is not None:
                    # Store as JSON array
                    project.embeddings = json.dumps(embedding.tolist())
                    
                    if update_db:
                        db.add(project)
                    
                    success_count += 1
                else:
                    error_count += 1
                    
            except Exception as e:
                logger.error(f"Error generating embedding for project {project.id}: {e}")
                error_count += 1
        
        if update_db:
            db.commit()
        
        logger.info(f"Embedding generation complete: {success_count} success, {error_count} errors")
        
        return {
            'total': len(projects),
            'success': success_count,
            'errors': error_count
        }


# Global service instance
embeddings_service = EmbeddingsService()


def find_similar_projects(project: Project, db: Session, top_k: int = 10) -> List[Dict]:
    """
    Convenience function to find similar projects
    
    Example:
        similar = find_similar_projects(my_project, db, top_k=5)
        for match in similar:
            print(f"{match['title']} - {match['similarity_score']:.2%} similar")
    """
    return embeddings_service.find_similar_projects(project, db, top_k)


def semantic_search(query: str, db: Session, tenant_id: int, **kwargs) -> List[Dict]:
    """
    Convenience function for semantic search
    
    Example:
        results = semantic_search(
            "large data center projects in texas",
            db,
            tenant_id=1,
            filters={'min_value': 50000000}
        )
    """
    return embeddings_service.semantic_search(query, db, tenant_id, **kwargs)
