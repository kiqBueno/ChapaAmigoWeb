from flask import Blueprint
from ..controllers.image_controller import image_controller
from ..controllers.pdf_controller import pdf_controller

image_bp = Blueprint('image', __name__)

@image_bp.route('/upload-image', methods=['POST'])
def upload_image():
    return image_controller.upload_image(pdf_controller)
