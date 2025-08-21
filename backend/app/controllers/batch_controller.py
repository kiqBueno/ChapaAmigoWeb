import os
import json
import logging
import zipfile
import tempfile
import threading
from datetime import datetime
from flask import request, jsonify, Response, send_file
from io import BytesIO
from ..services.pdf_service import processPdf
from ..services.extract_service import extractDataFromPdf
from ..services.batch_service import batch_manager, BatchStatus
from ..models.pdf_models import PdfProcessingRequest, ExtractedData
from ..utils.path_config import get_upload_path, get_batch_results_path
from ..config import Config

class BatchController:
    def __init__(self):
        self.processing_threads = {}
    
    def upload_batch_pdfs(self):
        """Upload multiple PDFs for batch processing"""
        try:
            files = request.files.getlist('files')
            if not files:
                return jsonify({"error": "No files provided."}), 400
            
            # Check file count limit
            if len(files) > Config.MAX_FILES_PER_BATCH:
                return jsonify({
                    "error": f"Too many files. Maximum {Config.MAX_FILES_PER_BATCH} files per batch."
                }), 400
            
            # Validate and save files
            uploaded_files = []
            total_size = 0
            
            for i, file in enumerate(files):
                if file.filename == '':
                    continue
                
                # Check file type
                if not file.filename or not file.filename.lower().endswith('.pdf'):
                    return jsonify({
                        "error": f"File {file.filename or 'unknown'} is not a PDF."
                    }), 400
                
                # Check individual file size
                file.seek(0, 2)  # Seek to end
                file_size = file.tell()
                file.seek(0)  # Reset to beginning
                
                if file_size > Config.MAX_FILE_SIZE:
                    return jsonify({
                        "error": f"File {file.filename} exceeds maximum size of {Config.MAX_FILE_SIZE / 1024 / 1024:.1f}MB."
                    }), 400
                
                total_size += file_size
                
                # Save file with unique name
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_path = get_upload_path(f'batch_{timestamp}_{i}_{file.filename}')
                file.save(file_path)
                
                # Extract data from PDF
                try:
                    extracted_data = extractDataFromPdf(file_path)
                    name = extracted_data.get("Nome", f"Unknown_{i}")
                except Exception as e:
                    logging.warning(f"Could not extract data from {file.filename}: {e}")
                    name = f"Unknown_{i}"
                
                uploaded_files.append({
                    "filename": file.filename,
                    "file_path": file_path,
                    "extracted_name": name,
                    "file_size": file_size
                })
            
            if not uploaded_files:
                return jsonify({"error": "No valid files uploaded."}), 400
            
            # Get processing options
            processing_options = {
                'password': request.form.get('password', Config.DEFAULT_PDF_PASSWORD),
                'use_watermark': request.form.get('useWatermark', 'true') == 'true',
                'include_contract': request.form.get('includeContract', 'true') == 'true',
                'include_documents': request.form.get('includeDocuments', 'true') == 'true',
                'selected_groups': json.loads(request.form.get('selectedGroups', '{}')),
                'summary_texts': json.loads(request.form.get('summaryTexts', '[]')),
                'image_path': None  # Will be set if image is uploaded
            }
            
            # Create batch job
            batch_id = batch_manager.create_batch_job(uploaded_files, processing_options)
            
            return jsonify({
                "batch_id": batch_id,
                "files_count": len(uploaded_files),
                "total_size_mb": round(total_size / 1024 / 1024, 2),
                "status": "uploaded",
                "message": f"Batch uploaded successfully. Use batch_id {batch_id} to start processing."
            })
            
        except Exception as e:
            logging.error(f"Error uploading batch PDFs: {e}")
            return jsonify({"error": str(e)}), 500
    
    def start_batch_processing(self):
        """Start processing a batch job"""
        try:
            data = request.get_json()
            batch_id = data.get('batch_id')
            
            if not batch_id:
                return jsonify({"error": "batch_id is required."}), 400
            
            job = batch_manager.get_job(batch_id)
            if not job:
                return jsonify({"error": "Batch job not found."}), 404
            
            if job.status != BatchStatus.PENDING:
                return jsonify({"error": f"Batch job is already {job.status.value}."}), 400
            
            # Start processing in background thread
            thread = threading.Thread(
                target=self._process_batch_background,
                args=(batch_id,),
                daemon=True
            )
            thread.start()
            self.processing_threads[batch_id] = thread
            
            # Update job status
            batch_manager.update_job_status(
                batch_id, 
                BatchStatus.PROCESSING,
                started_at=datetime.now().isoformat()
            )
            
            return jsonify({
                "batch_id": batch_id,
                "status": "processing_started",
                "message": "Batch processing started in background."
            })
            
        except Exception as e:
            logging.error(f"Error starting batch processing: {e}")
            return jsonify({"error": str(e)}), 500
    
    def _process_batch_background(self, batch_id: str):
        """Process batch in background thread"""
        try:
            job = batch_manager.get_job(batch_id)
            if not job:
                logging.error(f"Job {batch_id} not found for background processing")
                return
            
            logging.info(f"Starting background processing for batch {batch_id}")
            
            # Create result file path
            zip_path = get_batch_results_path(f"batch_{batch_id}.zip")
            
            # Process files and create ZIP
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                if not job.files or not job.processing_options:
                    logging.error(f"Job {batch_id} missing files or processing options")
                    return
                
                for i, file_info in enumerate(job.files):
                    try:
                        logging.info(f"Processing file {i+1}/{len(job.files)}: {file_info.filename}")
                        
                        # Process PDF
                        output_pdf = processPdf(
                            file=file_info.file_path,
                            password=job.processing_options.get('password', '515608'),
                            useWatermark=job.processing_options.get('use_watermark', True),
                            includeContract=job.processing_options.get('include_contract', True),
                            includeDocuments=job.processing_options.get('include_documents', True),
                            selectedGroups=job.processing_options.get('selected_groups', {}),
                            photoPath=job.processing_options.get('image_path'),
                            summaryTexts=job.processing_options.get('summary_texts', [])
                        )
                        
                        output_pdf.seek(0)
                        
                        # Generate filename
                        safe_name = file_info.extracted_name.replace(" ", "_")
                        filename = f"Relatorio_{safe_name}.pdf"
                        
                        # Add to ZIP
                        zip_file.writestr(filename, output_pdf.read())
                        
                        # Update file status
                        batch_manager.update_file_status(batch_id, i, "completed")
                        
                        logging.info(f"Successfully processed file {i+1}: {filename}")
                        
                    except Exception as e:
                        logging.error(f"Error processing file {i+1} ({file_info.filename}): {e}")
                        
                        # Create error file
                        error_filename = f"ERROR_{file_info.extracted_name.replace(' ', '_')}.txt"
                        error_content = f"Erro ao processar {file_info.filename}: {str(e)}"
                        zip_file.writestr(error_filename, error_content.encode('utf-8'))
                        
                        # Update file status with error
                        batch_manager.update_file_status(batch_id, i, "failed", str(e))
            
            # Update job completion
            batch_manager.update_job_status(
                batch_id,
                BatchStatus.COMPLETED,
                completed_at=datetime.now().isoformat(),
                result_zip_path=zip_path
            )
            
            logging.info(f"Batch {batch_id} processing completed. Result saved to {zip_path}")
            
        except Exception as e:
            logging.error(f"Error in background processing for batch {batch_id}: {e}")
            batch_manager.update_job_status(batch_id, BatchStatus.FAILED)
        finally:
            # Remove thread reference
            if batch_id in self.processing_threads:
                del self.processing_threads[batch_id]
    
    def get_batch_status(self):
        """Get status of a batch job"""
        try:
            batch_id = request.args.get('batch_id')
            if not batch_id:
                return jsonify({"error": "batch_id parameter is required."}), 400
            
            status = batch_manager.get_batch_status(batch_id)
            if not status:
                return jsonify({"error": "Batch job not found."}), 404
            
            return jsonify(status)
            
        except Exception as e:
            logging.error(f"Error getting batch status: {e}")
            return jsonify({"error": str(e)}), 500
    
    def download_batch_result(self):
        """Download the result ZIP file of a completed batch"""
        try:
            batch_id = request.args.get('batch_id')
            if not batch_id:
                return jsonify({"error": "batch_id parameter is required."}), 400
            
            job = batch_manager.get_job(batch_id)
            if not job:
                return jsonify({"error": "Batch job not found."}), 404
            
            if job.status != BatchStatus.COMPLETED:
                return jsonify({"error": f"Batch is not completed. Status: {job.status.value}"}), 400
            
            if not job.result_zip_path or not os.path.exists(job.result_zip_path):
                return jsonify({"error": "Result file not found."}), 404
            
            return send_file(
                job.result_zip_path,
                as_attachment=True,
                download_name=f"Relatorios_Batch_{batch_id}_{job.total_files}_files.zip",
                mimetype='application/zip'
            )
            
        except Exception as e:
            logging.error(f"Error downloading batch result: {e}")
            return jsonify({"error": str(e)}), 500
    
    def list_batch_jobs(self):
        """List all batch jobs"""
        try:
            limit = int(request.args.get('limit', 50))
            jobs = batch_manager.list_jobs(limit)
            
            return jsonify({
                "jobs": jobs,
                "total": len(jobs)
            })
            
        except Exception as e:
            logging.error(f"Error listing batch jobs: {e}")
            return jsonify({"error": str(e)}), 500
    
    def cancel_batch_job(self):
        """Cancel a batch job"""
        try:
            data = request.get_json()
            batch_id = data.get('batch_id')
            
            if not batch_id:
                return jsonify({"error": "batch_id is required."}), 400
            
            job = batch_manager.get_job(batch_id)
            if not job:
                return jsonify({"error": "Batch job not found."}), 404
            
            if job.status in [BatchStatus.COMPLETED, BatchStatus.FAILED, BatchStatus.CANCELLED]:
                return jsonify({"error": f"Cannot cancel job with status: {job.status.value}"}), 400
            
            batch_manager.update_job_status(batch_id, BatchStatus.CANCELLED)
            
            return jsonify({
                "batch_id": batch_id,
                "status": "cancelled",
                "message": "Batch job cancelled successfully."
            })
            
        except Exception as e:
            logging.error(f"Error cancelling batch job: {e}")
            return jsonify({"error": str(e)}), 500

batch_controller = BatchController()
