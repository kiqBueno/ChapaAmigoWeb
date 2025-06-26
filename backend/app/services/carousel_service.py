"""
Service for managing carousel images
"""
import os
import json
import logging
from typing import Dict, List, Optional
from ..utils.path_config import get_carousel_path
from ..models.carousel_models import CarouselImage

class CarouselService:
    """Service class for carousel management"""
    
    def __init__(self):
        self.carousel_path = get_carousel_path()
        self.config_path = os.path.join(self.carousel_path, 'carousel_config.json')
    
    def get_carousel_config(self) -> Dict:
        """Get carousel configuration"""
        try:
            if not os.path.exists(self.config_path):
                # Create default config if it doesn't exist
                default_config = {
                    "images": [
                        {"id": i, "filename": "", "isActive": False} 
                        for i in range(1, 9)
                    ]
                }
                self._save_config(default_config)
                return default_config
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            # Validate and fix configuration
            config = self._validate_carousel_config(config)
            return config
            
        except Exception as e:
            logging.error(f"Error getting carousel config: {e}")
            raise
    
    def upload_carousel_image(self, image_file, image_id: int) -> bool:
        """Upload a new carousel image"""
        try:
            if not (1 <= image_id <= 8):
                raise ValueError("Image ID must be between 1 and 8")
            
            # Save image file
            image_filename = f"carrousel{image_id}.jpg"
            image_path = os.path.join(self.carousel_path, image_filename)
            image_file.save(image_path)
            
            # Update configuration
            config = self.get_carousel_config()
            for img_info in config['images']:
                if img_info['id'] == image_id:
                    img_info['filename'] = image_filename
                    img_info['isActive'] = True
                    break
            
            self._save_config(config)
            return True
            
        except Exception as e:
            logging.error(f"Error uploading carousel image: {e}")
            raise
    
    def delete_carousel_image(self, image_id: int) -> bool:
        """Delete a carousel image"""
        try:
            if not (1 <= image_id <= 8):
                raise ValueError("Image ID must be between 1 and 8")
            
            # Delete image file
            image_filename = f"carrousel{image_id}.jpg"
            image_path = os.path.join(self.carousel_path, image_filename)
            
            if os.path.exists(image_path):
                os.remove(image_path)
            
            # Update configuration
            config = self.get_carousel_config()
            for img_info in config['images']:
                if img_info['id'] == image_id:
                    img_info['filename'] = ""
                    img_info['isActive'] = False
                    break
            
            self._save_config(config)
            return True
            
        except Exception as e:
            logging.error(f"Error deleting carousel image: {e}")
            raise
    
    def get_carousel_images(self) -> List[CarouselImage]:
        """Get list of carousel images"""
        try:
            config = self.get_carousel_config()
            images = []
            
            for img_info in config['images']:
                filename = img_info.get('filename', '')
                # Check if image file exists
                exists = False
                if filename:
                    image_path = os.path.join(self.carousel_path, filename)
                    exists = os.path.exists(image_path)
                
                images.append(CarouselImage(
                    id=img_info['id'],
                    filename=filename,
                    is_active=img_info.get('isActive', False),
                    exists=exists
                ))
            
            return images
            
        except Exception as e:
            logging.error(f"Error getting carousel images: {e}")
            raise
    
    def _save_config(self, config: Dict) -> None:
        """Save configuration to file"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def _validate_carousel_config(self, config: Dict) -> Dict:
        """Validate and fix carousel configuration to avoid duplicated filenames"""
        seen_filenames = {}
        
        for img_info in config['images']:
            filename = img_info.get('filename', '')
            if filename and filename in seen_filenames:
                # Duplicated filename found, clear it from this entry
                logging.warning(f"Duplicate filename {filename} found in ID {img_info['id']}, clearing it")
                img_info['filename'] = ""
                img_info['isActive'] = False
            elif filename:
                seen_filenames[filename] = img_info['id']
        
        return config
