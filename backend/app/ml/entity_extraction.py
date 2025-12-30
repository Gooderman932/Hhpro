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
