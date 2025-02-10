from flask import request, jsonify
from pydantic import ValidationError
from models import GamePayload
from utils.logger import logger

def request_validation_middleware(app):
    """Request validation middleware to validate incoming requests."""
    
    @app.before_request
    def validate_request():
        """Validate incoming JSON payload using Pydantic models."""
        if request.is_json:
            try:
                request_json = request.get_json()
                # Validate request payload using Pydantic model
                payload = GamePayload(**request_json)
                logger.debug("Request payload validated successfully.")
            except ValidationError as e:
                logger.warning("Invalid request payload: %s", e.json())
                return jsonify({"error": "Invalid payload", "details": e.errors()}), 400
        else:
            logger.warning("Request body is not JSON.")
            return jsonify({"error": "Invalid or missing JSON payload"}), 400
