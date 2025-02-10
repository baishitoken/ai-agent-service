import os
import subprocess
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the necessary paths for environment setup
VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"
CONFIG_FILE = "config.py"

def check_if_python_installed():
    """Check if Python is installed on the system."""
    try:
        python_version = subprocess.check_output(["python", "--version"], stderr=subprocess.STDOUT)
        logger.info(f"Python is installed: {python_version.decode('utf-8')}")
    except subprocess.CalledProcessError:
        logger.error("Python is not installed. Please install Python 3.x to continue.")
        sys.exit(1)

def check_if_pip_installed():
    """Check if pip is installed."""
    try:
        subprocess.check_output([sys.executable, "-m", "pip", "--version"])
        logger.info("pip is installed.")
    except subprocess.CalledProcessError:
        logger.error("pip is not installed. Please install pip to continue.")
        sys.exit(1)

def create_virtualenv():
    """Create a virtual environment in the project folder."""
    if not os.path.exists(VENV_DIR):
        logger.info(f"Creating virtual environment in {VENV_DIR}...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
        logger.info(f"Virtual environment created at {VENV_DIR}.")
    else:
        logger.info("Virtual environment already exists.")

def install_requirements():
    """Install the project dependencies listed in the requirements.txt file."""
    if os.path.exists(REQUIREMENTS_FILE):
        logger.info(f"Installing dependencies from {REQUIREMENTS_FILE}...")
        subprocess.check_call([os.path.join(VENV_DIR, "bin", "pip"), "install", "-r", REQUIREMENTS_FILE])
        logger.info("Dependencies installed successfully.")
    else:
        logger.error(f"{REQUIREMENTS_FILE} file is missing! Please create it to continue.")
        sys.exit(1)

def configure_config_file():
    """Check if the configuration file exists and prompt user to create it if missing."""
    if not os.path.exists(CONFIG_FILE):
        logger.warning(f"{CONFIG_FILE} is missing. Please provide the necessary configuration details.")
        create_default_config()

def create_default_config():
    """Create a default config file with placeholder settings."""
    config_content = """# Default config file

MONGODB_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "game_database"
SECRET_KEY = "your-secret-key"
DEBUG = True
"""
    try:
        with open(CONFIG_FILE, "w") as f:
            f.write(config_content)
        logger.info(f"Default config file created at {CONFIG_FILE}.")
    except Exception as e:
        logger.error(f"Error creating {CONFIG_FILE}: {e}")
        sys.exit(1)

def setup_environment():
    """Automate the environment setup for the project."""
    logger.info("Starting the environment setup process...")

    # Step 1: Check if Python and pip are installed
    check_if_python_installed()
    check_if_pip_installed()

    # Step 2: Create a virtual environment
    create_virtualenv()

    # Step 3: Install project dependencies
    install_requirements()

    # Step 4: Configure the project config file if necessary
    configure_config_file()

    logger.info("Environment setup complete!")

if __name__ == "__main__":
    setup_environment()
