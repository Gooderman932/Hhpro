"""Data utilities."""
from typing import Optional


def normalize_string(value: Optional[str]) -> Optional[str]:
    """Normalize a string value."""
    if value is None:
        return None
    return value.strip().title() if value else None


def parse_currency(value: str) -> Optional[float]:
    """Parse a currency string to float."""
    if not value:
        return None
    try:
        # Remove currency symbols and commas
        cleaned = value.replace("$", "").replace(",", "").strip()
        return float(cleaned)
    except ValueError:
        return None


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Validate latitude and longitude."""
    return -90 <= latitude <= 90 and -180 <= longitude <= 180
