from dataclasses import dataclass
import os

@dataclass
class FileUpload:
    filename: str
    filepath: str
    file_type: str
    file_size: int
    
    def exists(self) -> bool:
        return os.path.exists(self.filepath)
    
    def delete(self) -> bool:
        try:
            if self.exists():
                os.remove(self.filepath)
                return True
            return False
        except Exception:
            return False
