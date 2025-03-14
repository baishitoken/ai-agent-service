import os
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError
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

def get_collection(game):
    """Get the collection for the specific game."""
    client = get_db_connection()
    db = client[Config.DATABASE_NAME]
    collection_name = f"{game}_game_data"
    return db[collection_name]

def get_all_documents(game):
    """Retrieve all documents from a specific game's collection."""
    collection = get_collection(game)
    return list(collection.find())

def get_document_by_id(game, doc_id):
    """Retrieve a document by its ID."""
    collection = get_collection(game)
    return collection.find_one({"_id": doc_id})

def get_documents_by_field(game, field, value):
    """Retrieve documents based on a specific field and value."""
    collection = get_collection(game)
    return list(collection.find({field: value}))

def update_document(game, doc_id, update_data):
    """Update a specific document by its ID."""
    collection = get_collection(game)
    collection.update_one({"_id": doc_id}, {"$set": update_data})
    logger.info("Document with ID %s updated.", doc_id)

def update_documents_by_field(game, field, value, update_data):
    """Update multiple documents based on a field and value."""
    collection = get_collection(game)
    collection.update_many({field: value}, {"$set": update_data})
    logger.info("Documents with %s = %s updated.", field, value)

def delete_document(game, doc_id):
    """Delete a document by its ID."""
    collection = get_collection(game)
    collection.delete_one({"_id": doc_id})
    logger.info("Document with ID %s deleted.", doc_id)

def delete_documents_by_field(game, field, value):
    """Delete multiple documents based on a field and value."""
    collection = get_collection(game)
    collection.delete_many({field: value})
    logger.info("Documents with %s = %s deleted.", field, value)

def count_documents(game):
    """Count the total number of documents in a specific collection."""
    collection = get_collection(game)
    return collection.count_documents({})

def aggregate_documents(game, pipeline):
    """Perform aggregation operations on the collection."""
    collection = get_collection(game)
    return list(collection.aggregate(pipeline))

def create_index(game, field, direction=ASCENDING):
    """Create an index on a field in the collection."""
    collection = get_collection(game)
    collection.create_index([(field, direction)])
    logger.info("Index created on field: %s", field)

def drop_index(game, field):
    """Drop an index on a field in the collection."""
    collection = get_collection(game)
    collection.drop_index(field)
    logger.info("Index dropped on field: %s", field)

def check_for_duplicate(game, field, value):
    """Check if a document with a specific field value already exists (to avoid duplicates)."""
    collection = get_collection(game)
    return collection.count_documents({field: value}) > 0

def insert_if_not_exists(game, data):
    """Insert data only if it doesn't already exist in the collection (to avoid duplicates)."""
    collection = get_collection(game)
    try:
        if not check_for_duplicate(game, "some_field", data["some_field"]):  # Modify the check condition as needed
            collection.insert_one(data)
            logger.info("Data inserted.")
        else:
            logger.warning("Data already exists. Skipping insert.")
    except DuplicateKeyError:
        logger.error("Duplicate key error when inserting data.")
        raise

def find_one_or_default(game, filter_query, default=None):
    """Retrieve one document matching the query, or return a default value if not found."""
    collection = get_collection(game)
    return collection.find_one(filter_query) or default

def find_documents_with_projection(game, filter_query, projection):
    """Retrieve documents matching a query with a specified projection (fields to include)."""
    collection = get_collection(game)
    return list(collection.find(filter_query, projection))

def sort_documents(game, field, ascending=True):
    """Sort the documents by a specific field."""
    collection = get_collection(game)
    sort_order = ASCENDING if ascending else DESCENDING
    return list(collection.find().sort(field, sort_order))

def get_distinct_values(game, field):
    """Retrieve distinct values for a given field."""
    collection = get_collection(game)
    return collection.distinct(field)

def perform_transaction(operations):
    """Perform multiple database operations as a single transaction."""
    client = get_db_connection()
    db = client[Config.DATABASE_NAME]
    session = client.start_session()
    try:
        with session.start_transaction():
            for op in operations:
                op(db, session)  # op should be a callable that performs an operation
        session.commit_transaction()
        logger.info("Transaction committed.")
    except Exception as e:
        session.abort_transaction()
        logger.error("Transaction aborted due to error: %s", e)
        raise
    finally:
        client.close()

def create_user(game, username, password):
    """Create a new user (example use case)."""
    collection = get_collection(game)
    if not check_for_duplicate(game, "username", username):
        collection.insert_one({"username": username, "password": password})
        logger.info("User %s created.", username)
    else:
        logger.warning("User %s already exists.", username)

def add_bulk_documents(game, documents):
    """Insert multiple documents in bulk."""
    collection = get_collection(game)
    try:
        collection.insert_many(documents)
        logger.info("Bulk data inserted.")
    except Exception as e:
        logger.error("Error during bulk insert: %s", e)
        raise
