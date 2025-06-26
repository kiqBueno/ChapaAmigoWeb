import os

class Config:
    BASE_URL = "http://0.0.0.0:8080"
    # BASE_URL = "http://127.0.0.1:5000"
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # CORS configuration
    CORS_ORIGINS = ["https://chapaamigo.com.br", "http://localhost:5173", "http://127.0.0.1:5173"]
    
    # Default PDF password
    DEFAULT_PDF_PASSWORD = '515608'

