from flask import request, jsonify
from time import time
from utils.logger import logger

# Simple in-memory store for rate limiting (could be replaced with Redis or similar)
request_timestamps = {}

def rate_limit_middleware(app):
    """Rate limiting middleware to limit requests per minute."""
    
    RATE_LIMIT = 100  # Max 100 requests per minute
    TIME_WINDOW = 60  # Time window in seconds (1 minute)
    
    @app.before_request
    def limit_requests():
        """Limit requests to a specific rate."""
        user_ip = request.remote_addr
        current_time = time()
        
        # Initialize request history for the user
        if user_ip not in request_timestamps:
            request_timestamps[user_ip] = []
        
        # Clean up timestamps that are older than the time window
        request_timestamps[user_ip] = [t for t in request_timestamps[user_ip] if current_time - t < TIME_WINDOW]
        
        # If user has exceeded the rate limit, block the request
        if len(request_timestamps[user_ip]) >= RATE_LIMIT:
            logger.warning("Rate limit exceeded for IP: %s", user_ip)
            return jsonify({"error": "Rate limit exceeded, try again later."}), 429
        
        # Record the current request time
        request_timestamps[user_ip].append(current_time)
        logger.debug("Request from IP: %s within rate limit.", user_ip)
