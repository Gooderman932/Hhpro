"""Entity extraction service for NER and data extraction."""
from typing import Dict, List, Any
import re


class EntityExtractionService:
    """Service for extracting entities from text."""
    
    def __init__(self):
        # In production, this would use a pre-trained NER model
        # For now, use pattern matching
        pass
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities from text."""
        entities = {
            "companies": self._extract_companies(text),
            "locations": self._extract_locations(text),
            "values": self._extract_values(text),
            "dates": self._extract_dates(text),
        }
        return entities
    
    def _extract_companies(self, text: str) -> List[str]:
        """Extract company names from text."""
        # Simple pattern matching for company suffixes
        company_patterns = [
            r'\b[A-Z][a-zA-Z\s&]+(?:Inc\.?|LLC|Corp\.?|Corporation|Company|Co\.?)\b',
            r'\b[A-Z][a-zA-Z\s&]+Construction\b',
            r'\b[A-Z][a-zA-Z\s&]+Contractors?\b',
        ]
        
        companies = set()
        for pattern in company_patterns:
            matches = re.findall(pattern, text)
            companies.update(matches)
        
        return list(companies)
    
    def _extract_locations(self, text: str) -> List[str]:
        """Extract location information from text."""
        # US state abbreviations
        state_pattern = r'\b[A-Z]{2}\b'
        
        # City, State pattern
        city_state_pattern = r'\b[A-Z][a-zA-Z\s]+,\s*[A-Z]{2}\b'
        
        locations = []
        locations.extend(re.findall(city_state_pattern, text))
        
        return locations
    
    def _extract_values(self, text: str) -> List[Dict[str, Any]]:
        """Extract monetary values from text."""
        # Pattern for currency values
        value_patterns = [
            r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:million|M|billion|B)?',
        ]
        
        values = []
        for pattern in value_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                value_str = match.group(0)
                values.append({
                    "text": value_str,
                    "value": self._parse_value(value_str)
                })
        
        return values
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extract dates from text."""
        # Simple date patterns
        date_patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        
        return dates
    
    def _parse_value(self, value_str: str) -> float:
        """Parse a currency string to float."""
        # Remove currency symbols and spaces
        cleaned = value_str.replace("$", "").replace(",", "").strip()
        
        # Extract number
        number_match = re.search(r'[\d.]+', cleaned)
        if not number_match:
            return 0.0
        
        value = float(number_match.group())
        
        # Handle million/billion multipliers
        if re.search(r'million|M\b', value_str, re.IGNORECASE):
            value *= 1_000_000
        elif re.search(r'billion|B\b', value_str, re.IGNORECASE):
            value *= 1_000_000_000
        
        return value
"""
Entity extraction service using NER and LLM
Extracts companies, people, locations, dates, and financial info from unstructured text
"""
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import openai
from loguru import logger
import spacy
from app.config import settings

# Load spaCy model (download with: python -m spacy download en_core_web_lg)
try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    logger.warning("spaCy model not found. Run: python -m spacy download en_core_web_lg")
    nlp = None


class EntityExtractor:
    """
    Extracts structured entities from construction project documents
    """
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Construction-specific patterns
        self.company_suffixes = [
            r'\b(LLC|Inc|Corp|Corporation|Ltd|Limited|GmbH|AG|SA|SRL|BV)\b',
            r'\b(Company|Co\.|Construction|Contractors|Builders|Engineering)\b'
        ]
        
        self.financial_patterns = {
            'budget': r'\$[\d,]+(?:\.\d{2})?(?:\s?(?:million|billion|M|B|K))?',
            'square_feet': r'[\d,]+\s?(?:sf|sq\.?\s?ft\.?|square feet)',
            'units': r'[\d,]+\s?units?',
        }
    
    def extract_all(self, text: str, use_llm: bool = True) -> Dict:
        """
        Extract all entities from text using hybrid approach
        
        Args:
            text: Raw text from permits, tenders, news articles
            use_llm: Whether to use OpenAI for enhanced extraction
            
        Returns:
            Dictionary with extracted entities
        """
        entities = {
            'companies': [],
            'people': [],
            'locations': [],
            'dates': [],
            'financial': {},
            'project_details': {},
            'raw_entities': []
        }
        
        # 1. Rule-based extraction
        entities['financial'] = self._extract_financial(text)
        
        # 2. spaCy NER
        if nlp:
            spacy_entities = self._extract_with_spacy(text)
            entities['companies'].extend(spacy_entities.get('companies', []))
            entities['people'].extend(spacy_entities.get('people', []))
            entities['locations'].extend(spacy_entities.get('locations', []))
            entities['dates'].extend(spacy_entities.get('dates', []))
            entities['raw_entities'] = spacy_entities.get('raw', [])
        
        # 3. LLM-enhanced extraction (most accurate but costs API calls)
        if use_llm and settings.OPENAI_API_KEY:
            llm_entities = self._extract_with_llm(text)
            
            # Merge and deduplicate
            entities['companies'] = self._merge_dedupe(
                entities['companies'], 
                llm_entities.get('companies', [])
            )
            entities['people'] = self._merge_dedupe(
                entities['people'],
                llm_entities.get('people', [])
            )
            entities['project_details'] = llm_entities.get('project_details', {})
        
        # Clean and standardize
        entities = self._standardize_entities(entities)
        
        return entities
    
    def _extract_financial(self, text: str) -> Dict:
        """Extract financial information using regex"""
        financial = {}
        
        for key, pattern in self.financial_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                financial[key] = matches
        
        # Parse budget to float
        if 'budget' in financial and financial['budget']:
            budget_str = financial['budget'][0]
            financial['budget_parsed'] = self._parse_currency(budget_str)
        
        return financial
    
    def _parse_currency(self, text: str) -> Optional[float]:
        """Parse currency string to float"""
        try:
            # Remove $ and commas
            text = text.replace('$', '').replace(',', '').strip()
            
            # Handle millions/billions
            multiplier = 1
            text_lower = text.lower()
            if 'billion' in text_lower or text_lower.endswith('b'):
                multiplier = 1_000_000_000
                text = re.sub(r'\s?(billion|b)$', '', text_lower)
            elif 'million' in text_lower or text_lower.endswith('m'):
                multiplier = 1_000_000
                text = re.sub(r'\s?(million|m)$', '', text_lower)
            elif text_lower.endswith('k'):
                multiplier = 1_000
                text = re.sub(r'\s?k$', '', text_lower)
            
            value = float(text)
            return value * multiplier
        except:
            return None
    
    def _extract_with_spacy(self, text: str) -> Dict:
        """Extract entities using spaCy NER"""
        if not nlp:
            return {}
        
        doc = nlp(text)
        
        entities = {
            'companies': [],
            'people': [],
            'locations': [],
            'dates': [],
            'raw': []
        }
        
        for ent in doc.ents:
            entities['raw'].append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            })
            
            if ent.label_ == 'ORG':
                entities['companies'].append(ent.text)
            elif ent.label_ == 'PERSON':
                entities['people'].append(ent.text)
            elif ent.label_ in ['GPE', 'LOC']:
                entities['locations'].append(ent.text)
            elif ent.label_ == 'DATE':
                entities['dates'].append(ent.text)
        
        return entities
    
    def _extract_with_llm(self, text: str) -> Dict:
        """
        Use OpenAI to extract structured entities
        This is the most accurate but costs API credits
        """
        prompt = f"""Extract the following information from this construction project document:

Document:
{text[:3000]}  

Extract:
1. Companies mentioned (owners, general contractors, subcontractors, architects, engineers)
2. Key people (names and titles)
3. Project details (type, size, budget, timeline)
4. Locations

Return as JSON with this structure:
{{
    "companies": [
        {{"name": "Company Name", "role": "general_contractor|owner|subcontractor|architect|engineer|supplier"}}
    ],
    "people": [
        {{"name": "Person Name", "title": "Job Title", "company": "Company"}}
    ],
    "project_details": {{
        "project_type": "commercial|residential|industrial|infrastructure|data_center|logistics|healthcare|education",
        "estimated_value": 1000000,
        "square_feet": 50000,
        "units": 100,
        "start_date": "2025-Q1",
        "completion_date": "2026-Q2"
    }},
    "locations": ["City, State", "Address"]
}}

Only include information explicitly stated in the document. Use null for missing values."""

        try:
            response = self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert at extracting structured data from construction documents. Return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"LLM extraction failed: {e}")
            return {}
    
    def _merge_dedupe(self, list1: List, list2: List) -> List:
        """Merge and deduplicate entity lists"""
        # Convert to set for deduplication
        combined = set()
        
        for item in list1 + list2:
            if isinstance(item, str):
                combined.add(item.strip())
            elif isinstance(item, dict):
                # For dict items, use name as key
                combined.add(item.get('name', '').strip())
        
        return sorted(list(combined))
    
    def _standardize_entities(self, entities: Dict) -> Dict:
        """Clean and standardize extracted entities"""
        # Remove empty strings
        entities['companies'] = [c for c in entities['companies'] if c and len(c) > 2]
        entities['people'] = [p for p in entities['people'] if p and len(p) > 2]
        entities['locations'] = [l for l in entities['locations'] if l and len(l) > 2]
        
        # Remove duplicates (case-insensitive)
        entities['companies'] = list(set([c.title() for c in entities['companies']]))
        
        return entities
    
    def extract_company_metadata(self, company_name: str, context: str = None) -> Dict:
        """
        Extract additional metadata about a company
        """
        prompt = f"""Given this company name: "{company_name}"
        
Context: {context if context else 'None provided'}

Provide:
1. Company type (general_contractor, subcontractor, supplier, owner, developer, architect, engineer)
2. Likely specialties or trades
3. Approximate company size if mentioned (small, medium, large, enterprise)

Return as JSON:
{{
    "company_type": "type",
    "specialties": ["specialty1", "specialty2"],
    "size": "small|medium|large|enterprise",
    "confidence": 0.8
}}"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",  # Cheaper model for this task
                messages=[
                    {"role": "system", "content": "You are a construction industry expert. Return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Company metadata extraction failed: {e}")
            return {
                "company_type": "unknown",
                "specialties": [],
                "size": None,
                "confidence": 0
            }


# Global instance
entity_extractor = EntityExtractor()


def extract_entities(text: str, use_llm: bool = True) -> Dict:
    """
    Convenience function for entity extraction
    
    Example:
        entities = extract_entities(permit_text)
        print(entities['companies'])  # ['ABC Construction LLC', 'XYZ Architects']
    """
    return entity_extractor.extract_all(text, use_llm=use_llm)
