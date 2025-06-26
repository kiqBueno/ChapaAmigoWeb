"""
Image Routes - URL endpoints for image operations
"""
from flask import Blueprint
from ..controllers.image_controller import image_controller
from ..controllers.pdf_controller import pdf_controller

# Create blueprint for image routes
image_bp = Blueprint('image', __name__)

@image_bp.route('/upload-image', methods=['POST'])
def upload_image():
    """Upload image endpoint"""
    return image_controller.upload_image(pdf_controller)
