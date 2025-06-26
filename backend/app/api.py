"""
Legacy API file for backwards compatibility
This file imports the new MVC structure to maintain existing functionality
"""
from .app import app

# Import for backwards compatibility
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
