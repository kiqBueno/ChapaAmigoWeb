from flask import Blueprint
from ..controllers.pdf_controller import pdf_controller

pdf_bp = Blueprint('pdf', __name__)

@pdf_bp.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    return pdf_controller.upload_pdf()

@pdf_bp.route('/process-pdf', methods=['POST'])
def process_pdf():
    return pdf_controller.process_pdf()

@pdf_bp.route('/crop-pdf', methods=['POST'])
def crop_pdf():
    return pdf_controller.crop_pdf()
