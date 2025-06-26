from flask import Flask
from flask_cors import CORS
from .config import Config
from .utils.logging_config import setupLogging
from .views.pdf_routes import pdf_bp
from .views.image_routes import image_bp
from .views.carousel_routes import carousel_bp

def create_app():
    """Factory function to create Flask app"""
    setupLogging()
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure CORS
    CORS(app, resources={
        r"/*": {
            "origins": ["https://chapaamigo.com.br", "http://localhost:5173", "http://127.0.0.1:5173"], 
            "supports_credentials": True
        }
    })
    
    # Register blueprints
    app.register_blueprint(pdf_bp)
    app.register_blueprint(image_bp)
    app.register_blueprint(carousel_bp)
    
    @app.after_request
    def after_request(response):
        if response.mimetype == 'application/json':
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
        
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        return response
    
    return app

# For backwards compatibility with the current api.py structure
app = create_app()

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
