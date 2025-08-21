from flask import Blueprint
from ..controllers.batch_controller import batch_controller

batch_bp = Blueprint('batch', __name__)

# Batch processing routes
@batch_bp.route('/upload-batch-pdfs', methods=['POST'])
def upload_batch_pdfs():
    """Upload multiple PDFs for batch processing"""
    return batch_controller.upload_batch_pdfs()

@batch_bp.route('/start-batch-processing', methods=['POST'])
def start_batch_processing():
    """Start processing a batch job"""
    return batch_controller.start_batch_processing()

@batch_bp.route('/batch-status', methods=['GET'])
def get_batch_status():
    """Get status of a batch job"""
    return batch_controller.get_batch_status()

@batch_bp.route('/download-batch-result', methods=['GET'])
def download_batch_result():
    """Download the result ZIP file of a completed batch"""
    return batch_controller.download_batch_result()

@batch_bp.route('/list-batch-jobs', methods=['GET'])
def list_batch_jobs():
    """List all batch jobs"""
    return batch_controller.list_batch_jobs()

@batch_bp.route('/cancel-batch-job', methods=['POST'])
def cancel_batch_job():
    """Cancel a batch job"""
    return batch_controller.cancel_batch_job()
