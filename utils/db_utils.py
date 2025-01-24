import os
from pymongo import MongoClient
from config import Config
from utils.logger import logger

def get_db_connection():
    """Establish a connection to the MongoDB database."""
    connection_string = Config.MONGODB_URI
    if not connection_string:
        raise EnvironmentError("MONGODB_URI is not set in the configuration.")
    return MongoClient(connection_string)

def store_processed_data(data, game):
    """Store the processed game data in the database."""
    try:
        client = get_db_connection()
        db = client[Config.DATABASE_NAME]
        collection_name = f"{game}_game_data"
        collection = db[collection_name]

        if isinstance(data, list):
            logger.info("Inserting multiple documents into collection: %s", collection_name)
            collection.insert_many(data)
        else:
            logger.info("Inserting a single document into collection: %s", collection_name)
            collection.insert_one(data)

        logger.info("Data successfully stored in MongoDB collection: %s", collection_name)
    except Exception as e:
        logger.exception("An error occurred while storing data in the database.")
        raise
    finally:
        client.close()
        logger.info("Database connection closed.")
