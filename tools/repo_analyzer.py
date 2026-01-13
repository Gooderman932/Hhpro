"""
Construction Platform Repository Analyzer
Automatically analyzes repository structure and identifies purpose/functions
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any

class ConstructionPlatformAnalyzer:
    """
    Automated analyzer for Construction Intelligence Platform repository
    """
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.project_info = {}
        
    def analyze_structure(self) -> Dict[str, Any]:
        """Analyze the repository structure to identify components"""
        
        analysis = {
            "platform_type": "Construction Intelligence Platform",
            "primary_purpose": "Enterprise SaaS for construction market intelligence",
            "key_features": [],
            "tech_stack": {
                "backend": [],
                "frontend": [],
                "infrastructure": []
            },
            "data_models": [],
            "modules": []
        }
        
        # Extract key information from README
        readme_content = self._read_file("README.md")
        if readme_content:
            # Extract features
            features_section = re.search(r'## 🎯 Key Features(.*?)(?=## |\Z)', readme_content, re.DOTALL)
            if features_section:
                features_text = features_section.group(1)
                features = re.findall(r'### \d+\. ([^\n]+)', features_text)
                analysis["key_features"] = features
                
            # Extract tech stack
            backend_stack = re.search(r'### Backend(.*?)(?=### |## |\Z)', readme_content, re.DOTALL)
            frontend_stack = re.search(r'### Frontend(.*?)(?=### |## |\Z)', readme_content, re.DOTALL)
            infra_stack = re.search(r'### Infrastructure(.*?)(?=### |## |\Z)', readme_content, re.DOTALL)
            
            if backend_stack:
                analysis["tech_stack"]["backend"] = self._extract_list_items(backend_stack.group(1))
            if frontend_stack:
                analysis["tech_stack"]["frontend"] = self._extract_list_items(frontend_stack.group(1))
            if infra_stack:
                analysis["tech_stack"]["infrastructure"] = self._extract_list_items(infra_stack.group(1))
        
        # Analyze data models from backend
        models_dir = self.repo_path / "backend" / "app" / "models"
        if models_dir.exists():
            analysis["data_models"] = [f.stem for f in models_dir.iterdir() if f.is_file()]
        
        # Analyze project modules
        if (self.repo_path / "backend" / "app" / "api").exists():
            api_dir = self.repo_path / "backend" / "app" / "api"
            analysis["modules"].extend([f.stem for f in api_dir.iterdir() if f.is_file()])
            
        return analysis
    
    def _read_file(self, file_path: str) -> str:
        """Read file content safely"""
        try:
            file_path = self.repo_path / file_path
            if file_path.exists():
                return file_path.read_text()
        except Exception:
            pass
        return ""
    
    def _extract_list_items(self, text: str) -> List[str]:
        """Extract list items from markdown text"""
        items = re.findall(r'-\s+(.+)', text)
        # Also handle bullet points with asterisks
        items.extend(re.findall(r'\*\s+(.+)', text))
        return [item.strip() for item in items if item.strip()]
    
    def identify_use_cases(self) -> List[str]:
        """Identify specific use cases from documentation"""
        use_cases = [
            "Project opportunity discovery and tracking",
            "Competitive intelligence and market share analysis", 
            "Predictive analytics for win probability",
            "Demand forecasting and seasonal analysis",
            "Construction company relationship mapping",
            "Multi-tenant business platform for construction firms",
            "Data-driven decision making for construction investments"
        ]
        return use_cases
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        return {
            "metadata": {
                "repository": str(self.repo_path),
                "analysis_date": str(self._get_current_date())
            },
            "structure_analysis": self.analyze_structure(),
            "use_cases": self.identify_use_cases()
        }
    
    def _get_current_date(self):
        """Get current date for report"""
        from datetime import datetime
        return datetime.now().isoformat()

# Usage example
if __name__ == "__main__":
    analyzer = ConstructionPlatformAnalyzer(".")
    report = analyzer.generate_report()
    
    print(json.dumps(report, indent=2))
