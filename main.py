import os
import json
from flask import Flask, request, jsonify
from utils.db_utils import store_processed_data
from utils.data_processing import get_processor
from config import Config
from utils.logger import logger
from pydantic import ValidationError
from models import GamePayload

app = Flask(__name__)

@app.route('/process-game-data', methods=['POST'])
def process_game_data_endpoint():
    try:
        logger.info("Received request to process game data.")
        request_data = request.get_json()

        request_json = request.get_json()
        try:
            payload = GamePayload(**request_json)
        except ValidationError as e:
            logger.warning("Payload validation failed: %s", e.json())
            return jsonify({"error": "Invalid payload", "details": e.errors()}), 400

        game_type = request_data["game"]
        game_data = request_data["data"]

        logger.info("Processing data for game type: %s", game_type)
        processor = get_processor(game_type)

        if not processor:
            logger.error("No processor available for game type: %s", game_type)
            return jsonify({"error": f"No processor available for game type '{game_type}'"}), 400

        processed_data = processor(game_data)
        store_processed_data(processed_data, game_type)

        logger.info("Successfully processed and stored game data.")
        return jsonify({"message": "Data processed and stored successfully"}), 200

    except Exception as e:
        logger.exception("An error occurred while processing game data.")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.FLASK_PORT)
