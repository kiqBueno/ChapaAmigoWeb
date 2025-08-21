import os

class Config:
    BASE_URL = "http://0.0.0.0:8080"
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Increased limits for batch processing
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB max total request size
    MAX_FILES_PER_BATCH = 50  # Maximum files per batch
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB per individual file
    
    CORS_ORIGINS = ["https://chapaamigo.com.br", "http://localhost:5173", "http://127.0.0.1:5173"]
    
    DEFAULT_PDF_PASSWORD = '515608'
    
    # Batch processing settings
    BATCH_PROCESSING_ENABLED = True
    BATCH_TIMEOUT = 300  # 5 minutes timeout per batch