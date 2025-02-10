import sys
import os
import logging
from utils.logger import configure_logging
from utils.db_utils import connect_to_db, close_db_connection
from utils.data_processing import process_blackjack_data, process_chess_data, process_eight_ball_data
from models.blackjack_model import BlackjackGameData
from models.chess import ChessGameData
from models.eight_ball import EightBallGameData
from config import Config

# Setup the logging configuration
configure_logging()

# Initialize database connection
db_client = None

def main():
    global db_client
    
    try:
        # Load configuration
        logging.info("Loading configuration from config.py.")
        
        # Connect to the database
        db_client = connect_to_db()
        
        logging.info("Successfully connected to the database.")
        
        # Simulate loading game data (This could be replaced with real data loading logic)
        logging.info("Loading game data...")
        
        blackjack_data = load_sample_blackjack_data()
        chess_data = load_sample_chess_data()
        eight_ball_data = load_sample_eight_ball_data()
        
        # Process game data
        logging.info("Processing Blackjack data...")
        process_blackjack_data(blackjack_data)
        
        logging.info("Processing Chess data...")
        process_chess_data(chess_data)
        
        logging.info("Processing 8-ball data...")
        process_eight_ball_data(eight_ball_data)
        
        # Store processed data in the database
        logging.info("Storing processed data in the database...")
        store_processed_data_in_db(blackjack_data, "blackjack")
        store_processed_data_in_db(chess_data, "chess")
        store_processed_data_in_db(eight_ball_data, "eight_ball")
        
        logging.info("Data successfully stored in the database.")
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        # Close database connection
        if db_client:
            close_db_connection(db_client)
            logging.info("Database connection closed.")
        logging.info("Application finished.")

def load_sample_blackjack_data():
    # Simulating the loading of Blackjack game data
    # In a real scenario, this could be loading from a file, API, etc.
    return BlackjackGameData(players=[{
        "username": "player1",
        "games_played": 50,
        "games_won": 25,
        "games_lost": 20,
        "games_push": 5,
        "moves": [],
        "game_history": []
    }])

def load_sample_chess_data():
    # Simulating the loading of Chess game data
    return ChessGameData(players=[{
        "username": "player1",
        "rating": 1400,
        "games_played": 50,
        "games_won": 25,
        "games_lost": 20,
        "games_drawn": 5,
        "moves": [],
        "game_history": []
    }])

def load_sample_eight_ball_data():
    # Simulating the loading of 8-ball game data
    return EightBallGameData(players=[{
        "username": "player1",
        "games": 50,
        "games_won": 25,
        "games_lost": 20,
        "balls_potted": 70,
        "fouls": 5,
        "eightballs_potted": 10,
        "game_data": [],
        "game_history": []
    }])

def store_processed_data_in_db(data, game_type):
    logging.info(f"Storing {game_type} game data in the database...")

if __name__ == "__main__":
    main()
