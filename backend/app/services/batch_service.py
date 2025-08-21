import os
import json
import logging
import uuid
import time
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from ..utils.path_config import get_batch_storage_path

class BatchStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class BatchFile:
    filename: str
    file_path: str
    extracted_name: str
    status: str = "pending"
    error_message: Optional[str] = None
    processed_at: Optional[str] = None

@dataclass
class BatchJob:
    batch_id: str
    total_files: int
    processed_files: int
    failed_files: int
    status: BatchStatus
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    files: Optional[List[BatchFile]] = None
    processing_options: Optional[Dict] = None
    result_zip_path: Optional[str] = None
    
    def __post_init__(self):
        if self.files is None:
            self.files = []

class BatchManager:
    def __init__(self, storage_path: Optional[str] = None):
        if storage_path is None:
            storage_path = get_batch_storage_path()
        self.storage_path = storage_path
        self.jobs: Dict[str, BatchJob] = {}
        self._ensure_storage_directory()
        self._load_existing_jobs()
    
    def _ensure_storage_directory(self):
        """Ensure the batch storage directory exists"""
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path, exist_ok=True)
    
    def _load_existing_jobs(self):
        """Load existing jobs from storage"""
        try:
            jobs_file = os.path.join(self.storage_path, "jobs.json")
            if os.path.exists(jobs_file):
                with open(jobs_file, 'r', encoding='utf-8') as f:
                    jobs_data = json.load(f)
                    for job_id, job_data in jobs_data.items():
                        # Convert dict back to BatchJob
                        job_data['status'] = BatchStatus(job_data['status'])
                        files = [BatchFile(**file_data) for file_data in job_data.get('files', [])]
                        job_data['files'] = files
                        self.jobs[job_id] = BatchJob(**job_data)
        except Exception as e:
            logging.error(f"Error loading existing jobs: {e}")
    
    def _save_jobs(self):
        """Save jobs to storage"""
        try:
            jobs_file = os.path.join(self.storage_path, "jobs.json")
            jobs_data = {}
            for job_id, job in self.jobs.items():
                job_dict = asdict(job)
                job_dict['status'] = job.status.value
                jobs_data[job_id] = job_dict
            
            with open(jobs_file, 'w', encoding='utf-8') as f:
                json.dump(jobs_data, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            logging.error(f"Error saving jobs: {e}")
    
    def create_batch_job(self, files_info: List[Dict], processing_options: Dict) -> str:
        """Create a new batch job"""
        batch_id = str(uuid.uuid4())
        
        batch_files = []
        for file_info in files_info:
            batch_file = BatchFile(
                filename=file_info['filename'],
                file_path=file_info['file_path'],
                extracted_name=file_info['extracted_name']
            )
            batch_files.append(batch_file)
        
        batch_job = BatchJob(
            batch_id=batch_id,
            total_files=len(batch_files),
            processed_files=0,
            failed_files=0,
            status=BatchStatus.PENDING,
            created_at=datetime.now().isoformat(),
            files=batch_files,
            processing_options=processing_options
        )
        
        self.jobs[batch_id] = batch_job
        self._save_jobs()
        
        logging.info(f"Created batch job {batch_id} with {len(batch_files)} files")
        return batch_id
    
    def get_batch_status(self, batch_id: str) -> Optional[Dict]:
        """Get the status of a batch job"""
        job = self.jobs.get(batch_id)
        if not job:
            return None
        
        return {
            "batch_id": job.batch_id,
            "total_files": job.total_files,
            "processed_files": job.processed_files,
            "failed_files": job.failed_files,
            "status": job.status.value,
            "created_at": job.created_at,
            "started_at": job.started_at,
            "completed_at": job.completed_at,
            "progress_percentage": (job.processed_files / job.total_files * 100) if job.total_files > 0 else 0,
            "result_zip_path": job.result_zip_path
        }
    
    def update_job_status(self, batch_id: str, status: BatchStatus, **kwargs):
        """Update job status"""
        if batch_id in self.jobs:
            self.jobs[batch_id].status = status
            for key, value in kwargs.items():
                if hasattr(self.jobs[batch_id], key):
                    setattr(self.jobs[batch_id], key, value)
            self._save_jobs()
    
    def update_file_status(self, batch_id: str, file_index: int, status: str, error_message: Optional[str] = None):
        """Update individual file status"""
        job = self.jobs.get(batch_id)
        if job and job.files and file_index < len(job.files):
            file_obj = job.files[file_index]
            file_obj.status = status
            file_obj.processed_at = datetime.now().isoformat()
            
            if error_message:
                file_obj.error_message = error_message
                job.failed_files += 1
            else:
                job.processed_files += 1
            
            self._save_jobs()
    
    def get_job(self, batch_id: str) -> Optional[BatchJob]:
        """Get a specific batch job"""
        return self.jobs.get(batch_id)
    
    def list_jobs(self, limit: int = 50) -> List[Dict]:
        """List all batch jobs"""
        jobs_list = []
        for job in sorted(self.jobs.values(), key=lambda x: x.created_at, reverse=True)[:limit]:
            jobs_list.append(self.get_batch_status(job.batch_id))
        return jobs_list
    
    def cleanup_old_jobs(self, days_old: int = 7):
        """Clean up jobs older than specified days"""
        cutoff_time = time.time() - (days_old * 24 * 60 * 60)
        
        jobs_to_remove = []
        for job_id, job in self.jobs.items():
            job_time = datetime.fromisoformat(job.created_at).timestamp()
            if job_time < cutoff_time:
                jobs_to_remove.append(job_id)
                # Also remove result files
                if job.result_zip_path and os.path.exists(job.result_zip_path):
                    try:
                        os.remove(job.result_zip_path)
                    except Exception as e:
                        logging.error(f"Error removing old result file {job.result_zip_path}: {e}")
        
        for job_id in jobs_to_remove:
            del self.jobs[job_id]
        
        if jobs_to_remove:
            self._save_jobs()
            logging.info(f"Cleaned up {len(jobs_to_remove)} old batch jobs")

# Global batch manager instance
batch_manager = BatchManager()
