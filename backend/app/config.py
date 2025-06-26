import os

class Config:
    BASE_URL = "http://0.0.0.0:8080"
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    CORS_ORIGINS = ["https://chapaamigo.com.br", "http://localhost:5173", "http://127.0.0.1:5173"]
    
    DEFAULT_PDF_PASSWORD = '515608'