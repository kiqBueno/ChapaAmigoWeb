"""
Carousel Models
"""
from dataclasses import dataclass
from typing import Dict

@dataclass
class CarouselImage:
    """Model for carousel image"""
    id: int
    filename: str
    is_active: bool
    exists: bool = False
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON response"""
        return {
            "id": self.id,
            "filename": self.filename,
            "isActive": self.is_active,
            "exists": self.exists
        }
