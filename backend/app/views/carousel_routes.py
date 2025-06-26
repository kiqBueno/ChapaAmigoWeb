"""
Carousel Routes - URL endpoints for carousel operations
"""
from flask import Blueprint, send_file, jsonify
from ..controllers.carousel_controller import carousel_controller
from ..utils.path_config import get_carousel_path
import os
import logging

# Create blueprint for carousel routes
carousel_bp = Blueprint('carousel', __name__)

@carousel_bp.route('/carousel-config', methods=['GET'])
def get_carousel_config():
    """Get carousel configuration endpoint"""
    return carousel_controller.get_carousel_config()

@carousel_bp.route('/carousel-images', methods=['GET'])
def get_carousel_images():
    """Get carousel images endpoint"""
    return carousel_controller.get_carousel_images()

@carousel_bp.route('/upload-carousel-image', methods=['POST'])
def upload_carousel_image():
    """Upload carousel image endpoint"""
    return carousel_controller.upload_carousel_image()

@carousel_bp.route('/delete-carousel-image', methods=['POST'])
def delete_carousel_image():
    """Delete carousel image endpoint"""
    return carousel_controller.delete_carousel_image()

@carousel_bp.route('/carousel-image/<filename>')
def serve_carousel_image(filename):
    """Serve carousel images from the configured public path"""
    try:
        public_path = get_carousel_path()
        # Validar que o arquivo é uma imagem do carrossel
        if not filename.startswith('carrousel') or not filename.endswith('.jpg'):
            return jsonify({"error": "Invalid filename"}), 400
        
        image_path = os.path.join(public_path, filename)
        
        if os.path.exists(image_path):
            response = send_file(image_path, mimetype='image/jpeg')
            response.headers['Cache-Control'] = 'public, max-age=300'  # Cache por 5 minutos
            return response
        else:
            # Retornar imagem placeholder se não existir
            placeholder_path = os.path.join(public_path, 'placeholder-image.svg')
            if os.path.exists(placeholder_path):
                response = send_file(placeholder_path, mimetype='image/svg+xml')
                response.headers['Cache-Control'] = 'public, max-age=3600'  # Cache por 1 hora
                return response
            else:
                return jsonify({"error": "Image not found"}), 404
                
    except Exception as e:
        logging.error(f"Error serving carousel image {filename}: {e}")
        return jsonify({"error": str(e)}), 500

@carousel_bp.route('/toggle-carousel-image', methods=['POST'])
def toggle_carousel_image():
    """Toggle active status of a carousel image"""
    return carousel_controller.toggle_carousel_image()

@carousel_bp.route('/reorder-carousel-images', methods=['POST'])
def reorder_carousel_images():
    """Reorder carousel images"""
    return carousel_controller.reorder_carousel_images()
