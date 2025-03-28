import logging

# Set up logger for AI-related activities
ai_logger = logging.getLogger("AI")
ai_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
ai_logger.addHandler(handler)

def get_ai_logger():
    """Return the AI logger instance."""
    return ai_logger
