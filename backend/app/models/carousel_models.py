from dataclasses import dataclass
from typing import Dict

@dataclass
class CarouselImage:
    id: int
    filename: str
    is_active: bool
    exists: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "filename": self.filename,
            "isActive": self.is_active,
            "exists": self.exists
        }
