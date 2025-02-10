from flask import request, jsonify
from utils.logger import logger

def auth_middleware(app):
    """Authentication middleware to check for valid tokens."""
    
    @app.before_request
    def check_authentication():
        """Check if the request has a valid authentication token."""
        token = request.headers.get('Authorization')
        if not token or token != "expected_token":  # Replace with actual token logic
            logger.warning("Unauthorized request - Missing or invalid token.")
            return jsonify({"error": "Unauthorized"}), 401
        logger.debug("Valid token provided.")
