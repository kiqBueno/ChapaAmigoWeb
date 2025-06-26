import logging
from flask import request, jsonify
from ..services.carousel_service import CarouselService

class CarouselController:
    
    def __init__(self):
        self.carousel_service = CarouselService()
    
    def get_carousel_config(self):
        try:
            config = self.carousel_service.get_carousel_config()
            return jsonify(config)
        except Exception as e:
            logging.error(f"Error getting carousel config: {e}")
            return jsonify({"error": str(e)}), 500
    
    def upload_carousel_image(self):
        try:
            image = request.files.get('image')
            if not image:
                return jsonify({"error": "No image provided"}), 400
            
            image_id = request.form.get('imageId')
            if not image_id:
                return jsonify({"error": "imageId is required"}), 400
            
            try:
                image_id = int(image_id)
            except ValueError:
                return jsonify({"error": "imageId must be a number"}), 400
            
            if not (1 <= image_id <= 8):
                return jsonify({"error": "imageId must be between 1 and 8"}), 400
            
            self.carousel_service.upload_carousel_image(image, image_id)
            return jsonify({"message": "Image uploaded successfully"})
            
        except Exception as e:
            logging.error(f"Error uploading carousel image: {e}")
            return jsonify({"error": str(e)}), 500
    
    def delete_carousel_image(self):
        try:
            data = request.get_json()
            image_id = data.get('imageId')
            
            if image_id is None:
                return jsonify({"error": "imageId is required"}), 400
            
            if not (1 <= image_id <= 8):
                return jsonify({"error": "imageId must be between 1 and 8"}), 400
            
            self.carousel_service.delete_carousel_image(image_id)
            return jsonify({"message": "Image deleted successfully"})
            
        except Exception as e:
            logging.error(f"Error deleting carousel image: {e}")
            return jsonify({"error": str(e)}), 500
    
    def get_carousel_images(self):
        try:
            images = self.carousel_service.get_carousel_images()
            return jsonify({"images": [img.to_dict() for img in images]})
        except Exception as e:
            logging.error(f"Error getting carousel images: {e}")
            return jsonify({"error": str(e)}), 500
    
    def toggle_carousel_image(self):
        try:
            from flask import request
            data = request.get_json()
            image_id = data.get('imageId')
            is_active = data.get('isActive')
            
            if image_id is None or is_active is None:
                return jsonify({"error": "imageId and isActive are required"}), 400
            
            config = self.carousel_service.get_carousel_config()
            
            for img_info in config['images']:
                if img_info['id'] == image_id:
                    img_info['isActive'] = is_active
                    break
            
            self.carousel_service._save_config(config)
            
            return jsonify({"message": "Image status updated successfully"})
            
        except Exception as e:
            logging.error(f"Error toggling carousel image: {e}")
            return jsonify({"error": str(e)}), 500
    
    def reorder_carousel_images(self):
        try:
            from flask import request
            data = request.get_json()
            source_id = data.get('sourceId')
            target_id = data.get('targetId')
            
            if source_id is None or target_id is None:
                return jsonify({"error": "sourceId and targetId are required"}), 400
            
            config = self.carousel_service.get_carousel_config()
            
            source_img = None
            target_img = None
            source_index = -1
            target_index = -1
            
            for i, img in enumerate(config['images']):
                if img['id'] == source_id:
                    source_img = img.copy()
                    source_index = i
                elif img['id'] == target_id:
                    target_img = img.copy()
                    target_index = i
            
            if not source_img or not target_img or source_index == -1 or target_index == -1:
                return jsonify({"error": "Source or target image not found"}), 404
            
            source_filename = source_img['filename']
            source_alt = source_img.get('alt', '')
            source_isActive = source_img['isActive']
            
            target_filename = target_img['filename']
            target_alt = target_img.get('alt', '')
            target_isActive = target_img['isActive']
            
            config['images'][source_index]['filename'] = target_filename
            config['images'][source_index]['alt'] = target_alt
            config['images'][source_index]['isActive'] = target_isActive
            
            config['images'][target_index]['filename'] = source_filename
            config['images'][target_index]['alt'] = source_alt
            config['images'][target_index]['isActive'] = source_isActive
            
            logging.info(f"Reordering images: source_id={source_id}, target_id={target_id}")
            
            self.carousel_service._save_config(config)
            
            logging.info("Images reordered successfully")
            return jsonify({"message": "Images reordered successfully"})
            
        except Exception as e:
            logging.error(f"Error reordering carousel images: {e}")
            return jsonify({"error": str(e)}), 500

carousel_controller = CarouselController()
