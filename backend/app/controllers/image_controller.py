import os
import logging
from flask import request, jsonify
from ..utils.path_config import get_upload_path
from ..models.file_upload import FileUpload

class ImageController:
    def upload_image(self, pdf_controller=None):
        try:
            image = request.files.get('image')
            if not image:
                return jsonify({"error": "No image provided."}), 400

            uploaded_image_path = get_upload_path('uploaded_image.png')
            image.save(uploaded_image_path)
            
            file_upload = FileUpload(
                filename='uploaded_image.png',
                filepath=uploaded_image_path,
                file_type='image/png',
                file_size=os.path.getsize(uploaded_image_path)
            )
            
            if pdf_controller:
                pdf_controller.set_uploaded_image_path(uploaded_image_path)
            
            logging.info(f"Image uploaded successfully: {file_upload.filename}")
            return jsonify({"message": "Image uploaded successfully."})
            
        except Exception as e:
            logging.error(f"Error uploading image: {e}")
            return jsonify({"error": str(e)}), 500

image_controller = ImageController()
