import logging
import os
from logging.handlers import RotatingFileHandler
from config import Config

# Adjust log level and file path based on the configuration
LOG_LEVEL = getattr(logging, Config.LOG_LEVEL.upper(), logging.DEBUG)

# Directory for logs
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# File-based logging setup
file_handler = RotatingFileHandler(
    Config.LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3
)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
)

# Console logging setup
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
)

# Logger configuration
logging.basicConfig(level=LOG_LEVEL, handlers=[file_handler, console_handler])
logger = logging.getLogger("AI-Agent-Service")

# Function to add contextual logging
class ContextualFilter(logging.Filter):
    def __init__(self, **context):
        super().__init__()
        self.context = context

    def filter(self, record):
        for key, value in self.context.items():
            setattr(record, key, value)
        return True

def add_context_to_logger(logger, **context):
    """Attach context to the logger."""
    contextual_filter = ContextualFilter(**context)
    logger.addFilter(contextual_filter)

# Usage of contextual logging
logger = logging.getLogger("AI-Agent-Service")
add_context_to_logger(logger, application="AI-Agent-Service", environment=os.getenv("ENV", "development"))

# Custom log levels for fine-grained control
logging.addLevelName(15, "VERBOSE")

def verbose(self, message, *args, **kwargs):
    if self.isEnabledFor(15):
        self._log(15, message, args, **kwargs)

logging.Logger.verbose = verbose

# Example usage of different logging levels
if __name__ == "__main__":
    logger.info("This is an info message.")
    logger.debug("This is a debug message.")
    logger.error("This is an error message.")
    logger.warning("This is a warning message.")
    logger.verbose("This is a verbose message.")
    logger.critical("This is a critical message.")

# Structured logging for external systems
try:
    import json

    def structured_log(level, message, **kwargs):
        log_entry = {"level": level, "message": message, **kwargs}
        logger.log(level, json.dumps(log_entry))
except ImportError:
    logger.error("Failed to load JSON module for structured logging.")

# Metrics logging for performance tracking
import time

def log_performance(metric_name, start_time):
    duration = time.time() - start_time
    logger.info(f"Performance Metric: {metric_name} took {duration:.2f} seconds.")
