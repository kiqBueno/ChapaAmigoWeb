import os
import json
import logging
from flask import request, jsonify, Response
from io import BytesIO
from PyPDF2 import PdfWriter, PdfReader
from ..services.pdf_service import processPdf, cropPdf
from ..services.extract_service import extractDataFromPdf
from ..models.pdf_models import PdfProcessingRequest, ExtractedData
from ..models.file_upload import FileUpload
from ..utils.path_config import get_upload_path

class PdfController:    
    def __init__(self):
        self.uploaded_pdf_path = None
        self.uploaded_image_path = None
    
    def upload_pdf(self):
        try:
            file = request.files.get('file')
            if not file:
                return jsonify({"error": "No file provided."}), 400

            self.uploaded_image_path = None
            self.uploaded_pdf_path = get_upload_path('uploaded_pdf.pdf')
            file.save(self.uploaded_pdf_path)
            
            extracted_data = extractDataFromPdf(self.uploaded_pdf_path)
            logging.debug(f"Extracted data: {extracted_data}")
            
            result = ExtractedData(
                name=extracted_data.get("Nome", "Unknown"),
                data=extracted_data
            )
            
            return Response(
                json.dumps({
                    "name": result.name
                }, ensure_ascii=False),
                content_type="application/json"
            )
        except Exception as e:
            logging.error(f"Error uploading PDF: {e}")
            return jsonify({"error": str(e)}), 500
    
    def process_pdf(self):
        try:
            if not self.uploaded_pdf_path:
                return jsonify({"error": "No PDF uploaded."}), 400
            
            password = request.form.get('password', '515608')
            use_watermark = request.form.get('useWatermark', 'true') == 'true'
            include_contract = request.form.get('includeContract', 'true') == 'true'
            include_documents = request.form.get('includeDocuments', 'true') == 'true'
            selected_groups = json.loads(request.form.get('selectedGroups', '{}'))
            summary_texts = json.loads(request.form.get('summaryTexts', '[]'))
            
            processing_request = PdfProcessingRequest(
                password=password,
                use_watermark=use_watermark,
                include_contract=include_contract,
                include_documents=include_documents,
                selected_groups=selected_groups,
                summary_texts=summary_texts
            )
            
            current_photo_path = None
            if self.uploaded_image_path and os.path.exists(self.uploaded_image_path):
                current_photo_path = self.uploaded_image_path
                
            # Process PDF
            output_pdf = processPdf(
                file=self.uploaded_pdf_path,
                password=processing_request.password,
                useWatermark=processing_request.use_watermark,
                includeContract=processing_request.include_contract,
                includeDocuments=processing_request.include_documents,
                selectedGroups=processing_request.selected_groups or {},
                photoPath=current_photo_path,
                summaryTexts=processing_request.summary_texts or []
            )

            # Encrypt PDF
            encrypted_pdf = BytesIO()
            writer = PdfWriter()
            
            output_pdf.seek(0)
            reader = PdfReader(output_pdf)
            for page in reader.pages:
                writer.add_page(page)
                
            writer.encrypt(processing_request.password)
            writer.write(encrypted_pdf)
            encrypted_pdf.seek(0)

            return Response(
                encrypted_pdf.read(),
                mimetype='application/pdf',
                headers={
                    'Content-Disposition': 'attachment; filename="processed_document.pdf"'
                }
            )
            
        except Exception as e:
            logging.error(f"Error processing PDF: {e}")
            return jsonify({"error": str(e)}), 500
    
    def crop_pdf(self):
        try:
            if not self.uploaded_pdf_path:
                return jsonify({"error": "No PDF uploaded."}), 400
            
            data = request.get_json()
            page_number = data.get('pageNumber', 1)
            crop_box = data.get('cropBox', {})
            password = data.get('password', '515608')
            
            with open(self.uploaded_pdf_path, 'rb') as f:
                pdf_content = BytesIO(f.read())
            
            result = cropPdf(pdf_content)
            
            return jsonify(result)
            
        except Exception as e:
            logging.error(f"Error cropping PDF: {e}")
            return jsonify({"error": str(e)}), 500
    
    def set_uploaded_image_path(self, path):
        self.uploaded_image_path = path

pdf_controller = PdfController()