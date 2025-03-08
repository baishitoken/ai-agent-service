import os
import json
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.db_utils import store_processed_data
from utils.data_processing import get_processor
from config import Config
from utils.logger import logger
from pydantic import ValidationError
from models import GamePayload

app = Flask(__name__)
CORS(app)  # Enable CORS

# Log the environment at startup
logger.info(f"Starting application in {Config.ENV} environment")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the service is running."""
    logger.debug("Health check requested.")
    return jsonify({"status": "healthy", "environment": Config.ENV}), 200


@app.errorhandler(400)
def bad_request_error(error):
    """Handle 400 Bad Request errors."""
    logger.warning("Bad request error: %s", error)
    return jsonify({"error": "Bad Request", "details": str(error)}), 400


@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 Internal Server errors."""
    logger.exception("Internal server error: %s", error)
    return jsonify({"error": "Internal Server Error", "details": str(error)}), 500


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


@app.route('/api/v1/process-game-data', methods=['POST'])
def process_game_data():
    start_time = time.time()
    try:
        logger.info("Received request to process game data.")
        request_json = request.get_json()

        if not request_json:
            logger.warning("Missing or invalid JSON payload.")
            return jsonify({"error": "Invalid or missing JSON payload"}), 400

        # Validate payload using Pydantic
        try:
            payload = GamePayload(**request_json)
        except ValidationError as e:
            logger.warning("Payload validation failed: %s", e.json())
            return jsonify({"error": "Invalid payload", "details": e.errors()}), 400

        game_type = payload.game
        game_data = payload.data

        logger.info("Processing data for game type: %s", game_type)
        processor = get_processor(game_type)

        if not processor:
            logger.error("No processor available for game type: %s", game_type)
            return jsonify({"error": f"No processor available for game type '{game_type}'"}), 400

        # Process and store the data
        processed_data = processor(game_data)
        store_processed_data(processed_data, game_type)

        logger.info("Successfully processed and stored game data.")
        response = jsonify({"message": "Data processed and stored successfully"})
        response.status_code = 200
        return response

    except Exception as e:
        logger.exception("An error occurred while processing game data.")
        return jsonify({"error": str(e)}), 500
    finally:
        duration = time.time() - start_time
        logger.info("Request processing time: %.2f seconds", duration)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.FLASK_PORT, debug=Config.FLASK_DEBUG)