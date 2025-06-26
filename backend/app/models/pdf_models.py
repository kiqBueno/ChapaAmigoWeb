"""
PDF Processing Models
"""
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class PdfProcessingRequest:
    """Model for PDF processing request"""
    password: str = '515608'
    use_watermark: bool = True
    include_contract: bool = True
    include_documents: bool = True
    selected_groups: Optional[Dict] = None
    summary_texts: Optional[List] = None
    
    def __post_init__(self):
        if self.selected_groups is None:
            self.selected_groups = {}
        if self.summary_texts is None:
            self.summary_texts = []

@dataclass
class ExtractedData:
    """Model for extracted PDF data"""
    name: str
    data: Dict
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON response"""
        return {
            "name": self.name,
            "data": self.data
        }
