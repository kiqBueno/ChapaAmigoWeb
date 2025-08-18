import os
import json
import logging
import zipfile
import tempfile
from flask import request, jsonify, Response
from io import BytesIO
from PyPDF2 import PdfWriter, PdfReader
from ..services.pdf_service import processPdf
from ..services.extract_service import extractDataFromPdf
from ..models.pdf_models import PdfProcessingRequest, ExtractedData
from ..models.file_upload import FileUpload
from ..utils.path_config import get_upload_path

class PdfController:    
    def __init__(self):
        self.uploaded_pdf_path = None
        self.uploaded_image_path = None
        self.extracted_name = None
        self.uploaded_multiple_files = []
        self.extracted_names = []
    
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
            
            self.extracted_name = result.name
            
            return Response(
                json.dumps({
                    "name": result.name
                }, ensure_ascii=False),
                content_type="application/json"
            )
        except Exception as e:
            logging.error(f"Error uploading PDF: {e}")
            return jsonify({"error": str(e)}), 500
    
    def upload_multiple_pdfs(self):
        try:
            files = request.files.getlist('files')
            if not files:
                return jsonify({"error": "No files provided."}), 400

            uploaded_files = []
            extracted_names = []
            
            for i, file in enumerate(files):
                if file.filename == '':
                    continue
                    
                # Salvar cada arquivo com um nome único
                file_path = get_upload_path(f'uploaded_pdf_{i}.pdf')
                file.save(file_path)
                
                # Extrair dados de cada arquivo
                extracted_data = extractDataFromPdf(file_path)
                logging.debug(f"Extracted data from file {i}: {extracted_data}")
                
                name = extracted_data.get("Nome", f"Unknown_{i}")
                uploaded_files.append({
                    "index": i,
                    "filename": file.filename,
                    "path": file_path,
                    "extracted_name": name
                })
                extracted_names.append(name)
            
            # Armazenar informações dos arquivos múltiplos
            self.uploaded_multiple_files = uploaded_files
            self.extracted_names = extracted_names
            
            return Response(
                json.dumps({
                    "files_count": len(uploaded_files),
                    "extracted_names": extracted_names
                }, ensure_ascii=False),
                content_type="application/json"
            )
        except Exception as e:
            logging.error(f"Error uploading multiple PDFs: {e}")
            return jsonify({"error": str(e)}), 500
    
    def process_pdf(self):
        try:
            # Check if we have multiple files or a single file
            if self.uploaded_multiple_files:
                # Process multiple PDFs
                return self._process_multiple_pdfs()
            elif self.uploaded_pdf_path:
                # Process single PDF
                return self._process_single_pdf()
            else:
                return jsonify({"error": "No PDF uploaded."}), 400
            
        except Exception as e:
            logging.error(f"Error processing PDF: {e}")
            return jsonify({"error": str(e)}), 500
    
    def _process_single_pdf(self):
        """Process a single PDF file"""
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
            
        # Ensure we have a valid PDF path
        if not self.uploaded_pdf_path:
            return jsonify({"error": "No PDF file available for processing."}), 400
            
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

        output_pdf.seek(0)

        safe_name = self.extracted_name.replace(" ", "_") if self.extracted_name else "processed_document"
        filename = f"Relatorio_{safe_name}.pdf"

        return Response(
            output_pdf.read(),
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
        )
    
    def _process_multiple_pdfs(self):
        """Process multiple PDF files and return them as a ZIP file or single PDF if only one file"""
        password = request.form.get('password', '515608')
        use_watermark = request.form.get('useWatermark', 'true') == 'true'
        include_contract = request.form.get('includeContract', 'true') == 'true'
        include_documents = request.form.get('includeDocuments', 'true') == 'true'
        selected_groups = json.loads(request.form.get('selectedGroups', '{}'))
        summary_texts = json.loads(request.form.get('summaryTexts', '[]'))
        
        if not self.uploaded_multiple_files:
            return jsonify({"error": "No multiple files available for processing."}), 400
        
        current_photo_path = None
        if self.uploaded_image_path and os.path.exists(self.uploaded_image_path):
            current_photo_path = self.uploaded_image_path
        
        # If only one file, return it as a single PDF
        if len(self.uploaded_multiple_files) == 1:
            file_info = self.uploaded_multiple_files[0]
            try:
                output_pdf = processPdf(
                    file=file_info["path"],
                    password=password,
                    useWatermark=use_watermark,
                    includeContract=include_contract,
                    includeDocuments=include_documents,
                    selectedGroups=selected_groups or {},
                    photoPath=current_photo_path,
                    summaryTexts=summary_texts or []
                )
                
                output_pdf.seek(0)
                
                # Generate filename for the single PDF
                safe_name = file_info["extracted_name"].replace(" ", "_") if file_info["extracted_name"] else "processed_document"
                filename = f"Relatorio_{safe_name}.pdf"
                
                return Response(
                    output_pdf.read(),
                    mimetype='application/pdf',
                    headers={
                        'Content-Disposition': f'attachment; filename="{filename}"'
                    }
                )
                
            except Exception as e:
                logging.error(f"Error processing single file: {e}")
                return jsonify({"error": f"Error processing file: {str(e)}"}), 500
        
        # For multiple files, create a ZIP file in memory
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for i, file_info in enumerate(self.uploaded_multiple_files):
                try:
                    # Process each PDF individually
                    output_pdf = processPdf(
                        file=file_info["path"],
                        password=password,
                        useWatermark=use_watermark,
                        includeContract=include_contract,
                        includeDocuments=include_documents,
                        selectedGroups=selected_groups or {},
                        photoPath=current_photo_path,
                        summaryTexts=summary_texts or []
                    )
                    
                    output_pdf.seek(0)
                    
                    # Generate filename for each processed PDF
                    safe_name = file_info["extracted_name"].replace(" ", "_") if file_info["extracted_name"] else f"processed_document_{i+1}"
                    filename = f"Relatorio_{safe_name}.pdf"
                    
                    # Add the processed PDF to the ZIP file
                    zip_file.writestr(filename, output_pdf.read())
                    
                    logging.info(f"Successfully processed file {i+1}: {filename}")
                    
                except Exception as e:
                    logging.error(f"Error processing file {i+1} ({file_info.get('filename', 'unknown')}): {e}")
                    # Create an error PDF for this file
                    error_filename = f"ERROR_Relatorio_{file_info.get('extracted_name', f'file_{i+1}').replace(' ', '_')}.txt"
                    error_content = f"Erro ao processar o arquivo {file_info.get('filename', 'unknown')}: {str(e)}"
                    zip_file.writestr(error_filename, error_content.encode('utf-8'))
        
        zip_buffer.seek(0)
        
        # Create filename for the ZIP file
        files_count = len(self.uploaded_multiple_files)
        zip_filename = f"Relatorios_Multiple_Files_{files_count}_pessoas.zip"
        
        return Response(
            zip_buffer.read(),
            mimetype='application/zip',
            headers={
                'Content-Disposition': f'attachment; filename="{zip_filename}"'
            }
        )
    
    def process_multiple_pdfs_individually(self):
        """Process multiple PDF files and return them one by one (for separate downloads)"""
        try:
            password = request.form.get('password', '515608')
            use_watermark = request.form.get('useWatermark', 'true') == 'true'
            include_contract = request.form.get('includeContract', 'true') == 'true'
            include_documents = request.form.get('includeDocuments', 'true') == 'true'
            selected_groups = json.loads(request.form.get('selectedGroups', '{}'))
            summary_texts = json.loads(request.form.get('summaryTexts', '[]'))
            file_index = int(request.form.get('file_index', 0))
            
            if not self.uploaded_multiple_files or file_index >= len(self.uploaded_multiple_files):
                return jsonify({"error": "Invalid file index or no files available."}), 400
            
            file_info = self.uploaded_multiple_files[file_index]
            
            current_photo_path = None
            if self.uploaded_image_path and os.path.exists(self.uploaded_image_path):
                current_photo_path = self.uploaded_image_path
            
            output_pdf = processPdf(
                file=file_info["path"],
                password=password,
                useWatermark=use_watermark,
                includeContract=include_contract,
                includeDocuments=include_documents,
                selectedGroups=selected_groups or {},
                photoPath=current_photo_path,
                summaryTexts=summary_texts or []
            )
            
            output_pdf.seek(0)
            
            # Generate filename for the processed PDF
            safe_name = file_info["extracted_name"].replace(" ", "_") if file_info["extracted_name"] else f"processed_document_{file_index+1}"
            filename = f"Relatorio_{safe_name}.pdf"
            
            return Response(
                output_pdf.read(),
                mimetype='application/pdf',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )
            
        except Exception as e:
            logging.error(f"Error processing individual PDF at index {file_index}: {e}")
            return jsonify({"error": str(e)}), 500


    
    def set_uploaded_image_path(self, path):
        self.uploaded_image_path = path

pdf_controller = PdfController()