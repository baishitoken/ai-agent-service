import os
import math
import time
import datetime
import logging

from flask import Flask, request
from flask_socketio import SocketIO, emit
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure

# ---------------------------------------------------------------------
# Configuration and Logging Setup
# ---------------------------------------------------------------------
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("8BallWS")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
socketio = SocketIO(app, cors_allowed_origins="*")

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'game_database')
COLLECTION_NAME = "eight_ball_game_data"

# ---------------------------------------------------------------------
# Database Utility Functions
# ---------------------------------------------------------------------
def get_db_connection():
    """
    Establish a connection to the MongoDB database.
    Raises an EnvironmentError if the connection string is not set.
    """
    try:
        client = MongoClient(MONGODB_URI)
        client.admin.command('ismaster')
        logger.debug("Connected to MongoDB successfully.")
        return client
    except ConnectionFailure as e:
        logger.error("Could not connect to MongoDB: %s", e)
        raise

def store_shot_data(processed_data):
    """
    Store processed shot trajectory data into the MongoDB collection.
    """
    client = None
    try:
        client = get_db_connection()
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        collection.insert_one(processed_data)
        logger.info("Processed shot data stored in MongoDB.")
    except Exception as e:
        logger.exception("Error storing shot data in MongoDB: %s", e)
    finally:
        if client:
            client.close()
            logger.debug("MongoDB connection closed.")

# ---------------------------------------------------------------------
# Shot Trajectory Processing Function
# ---------------------------------------------------------------------
def process_shot_trajectory(shot_data):
    """
    Process incoming shot data and calculate the predicted shot trajectory.
    
    Expected input (shot_data):
        {
            "player_id": "player_123",
            "timestamp": <unix_timestamp>,
            "cue_ball_position": [x, y],
            "power": <float>,
            "angle": <float>,   # in degrees
            "shot_attempts": <int>,
            "balls_potted": <int>,
            "fouls": <int>
        }
    
    Returns a dictionary with additional calculated fields:
        {
            ... original shot data ...,
            "predicted_path": [[x0, y0], [x1, y1], ..., [xN, yN]],
            "computed_end_position": [x_end, y_end],
            "processing_time": <seconds>
        }
    """
    start_time = time.time()

    try:
        cue_position = shot_data.get("cue_ball_position", [0, 0])
        power = shot_data.get("power", 0)
        angle_deg = shot_data.get("angle", 0)
        
        angle_rad = math.radians(angle_deg)
        
        distance = power * 0.5
        x_end = cue_position[0] + distance * math.cos(angle_rad)
        y_end = cue_position[1] + distance * math.sin(angle_rad)
        
        num_points = 10
        predicted_path = []
        for i in range(num_points + 1):
            t = i / num_points
            x = cue_position[0] + t * (x_end - cue_position[0])
            y = cue_position[1] + t * (y_end - cue_position[1])
            predicted_path.append([x, y])
        
        processing_time = time.time() - start_time

        processed_data = shot_data.copy()
        processed_data["computed_end_position"] = [x_end, y_end]
        processed_data["predicted_path"] = predicted_path
        processed_data["processing_time"] = processing_time

        logger.debug("Shot trajectory processed: End position [%f, %f]", x_end, y_end)
        logger.debug("Predicted path: %s", predicted_path)
        logger.debug("Processing time: %.4f seconds", processing_time)

        return processed_data
    except Exception as e:
        logger.exception("Error processing shot trajectory: %s", e)
        raise

# ---------------------------------------------------------------------
# WebSocket Event Handlers
# ---------------------------------------------------------------------
@socketio.on('connect')
def handle_connect():
    """
    Handle new client connection.
    """
    logger.info("Client connected: %s", request.sid)
    emit("connection_response", {"message": "Connected to 8-ball WebSocket server."})

@socketio.on('disconnect')
def handle_disconnect():
    """
    Handle client disconnection.
    """
    logger.info("Client disconnected: %s", request.sid)

@socketio.on('shot_data')
def handle_shot_data(data):
    """
    Handle incoming shot data from the WebGL client.
    
    Expects data in JSON format containing 8-ball shot details.
    Processes the shot trajectory and stores the result in MongoDB.
    """
    logger.info("Received shot_data event from client: %s", request.sid)
    logger.debug("Raw shot data: %s", data)
    
    try:
        # Process the shot trajectory using our defined function
        processed_data = process_shot_trajectory(data)
        
        # Optionally, you could emit a response back to the client with the computed trajectory
        emit("shot_data_processed", {"status": "success", "data": processed_data}, broadcast=False)
        
        # Store the processed data in the database
        store_shot_data(processed_data)
    except Exception as e:
        logger.exception("Error handling shot_data event: %s", e)
        emit("shot_data_processed", {"status": "error", "error": str(e)}, broadcast=False)

@socketio.on('ping_server')
def handle_ping(data):
    """
    Simple handler for ping events from the client.
    """
    logger.info("Received ping from client: %s", request.sid)
    emit("pong", {"message": "Pong!"})

# ---------------------------------------------------------------------
# HTTP Routes
# ---------------------------------------------------------------------
@app.route('/')
def index():
    """
    Basic HTTP route to check server status.
    """
    return "8-ball WebSocket Server is running."

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "timestamp": str(datetime.datetime.utcnow())}, 200

# ---------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------
def main():
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)