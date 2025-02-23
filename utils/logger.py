import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format="%(asctime)s [%(levelname)s] %(message)s",  # Log format
    handlers=[
        logging.StreamHandler()  # Output logs to the console
    ]
)

# Logger instance
logger = logging.getLogger(__name__)
