import time
from flask import request, jsonify
from utils.logger import logger

def logging_middleware(app):
    """Logging middleware to log requests and responses."""
    
    @app.before_request
    def before_request_logging():
        """Log incoming request details."""
        logger.debug("Incoming request: %s %s", request.method, request.url)
        logger.debug("Request headers: %s", dict(request.headers))
        if request.is_json:
            logger.debug("Request JSON body: %s", request.get_json())

    @app.after_request
    def after_request_logging(response):
        """Log outgoing response details."""
        logger.debug("Outgoing response status: %s", response.status)
        logger.debug("Outgoing response data: %s", response.get_data(as_text=True))
        return response
