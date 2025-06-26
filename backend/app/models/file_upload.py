"""
File Upload Model
"""
from dataclasses import dataclass
import os

@dataclass
class FileUpload:
    """Model for uploaded files"""
    filename: str
    filepath: str
    file_type: str
    file_size: int
    
    def exists(self) -> bool:
        """Check if file exists on disk"""
        return os.path.exists(self.filepath)
    
    def delete(self) -> bool:
        """Delete file from disk"""
        try:
            if self.exists():
                os.remove(self.filepath)
                return True
            return False
        except Exception:
            return False
