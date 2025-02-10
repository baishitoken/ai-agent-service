from flask import request, jsonify

def cors_middleware(app):
    """Middleware to handle CORS (Cross-Origin Resource Sharing)."""
    
    @app.after_request
    def add_cors_headers(response):
        """Allow requests from all origins or specify allowed origins."""
        response.headers['Access-Control-Allow-Origin'] = '*'  # Allow all origins (or specify allowed origins)
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
