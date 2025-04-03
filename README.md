# ![BAISHI](https://i.imgur.com/Z2DDroP.png) BAISHI AI AGENT DATA PROCESSOR SERVICE ![BAISHI](https://i.imgur.com/Z2DDroP.png)

## Introduction

BAISHI AI AGENT DATA PROCESSOR SERVICE is a modular, scalable service designed to process game data for various games such as 8-ball pool, chess, and more. The service ingests raw game data, processes it to extract actionable insights, and stores the results in a MongoDB database for further analysis or integration into downstream applications.

Built with Python, the service leverages Flask for API endpoints and WebSocket communication, Pydantic for schema validation, and MongoDB for persistent storage. Additionally, advanced AI and ML modules have been integrated to provide predictive capabilities and refined analytics for gameplay improvement.

---

## Features

- **Game-Agnostic Architecture**: Supports multiple games with separate models and processors for each.
- **Data Validation**: Uses Pydantic models to ensure that incoming payloads are clean and well-structured.
- **MongoDB Integration**: Processes and stores game data efficiently in dedicated MongoDB collections.
- **WebSocket Server**: Real-time communication with WebGL clients for shot trajectory processing.
- **AI & Machine Learning**:
  - **Reinforcement Learning**: A simple RL agent refines 8-ball shot selection based on game outcomes.
  - **Neural Network Training**: An extensive model training pipeline using PyTorch for 8-ball gameplay prediction.
  - **Playstyle Classification**: Uses Scikit-Learn to classify 8-ball players into Aggressive, Defensive, or Calculated playstyles.
- **Post-Game Analysis**: Extracts post-game summaries, analyzes trends, and adjusts AI model parameters for future predictions.
- **Spectator Mode**: An observation mode where the AI bot refines its strategy by observing five games before unlocking its full capabilities.
- **Logging & Error Handling**: Extensive logging with Python’s `logging` module and robust error handling for easier debugging.
- **Modular & Extensible Design**: Easily extend support for new games by adding Pydantic models and game-specific processors.
- **Unit Testing**: Comprehensive test suite covering key components, ensuring code quality and reliability.

---

## File Structure

```
/AI-AGENT-SERVICE
  ├── models/               # Pydantic models for games
  │   ├── eight_ball.py
  │   ├── chess.py
  │   └── game_models/      # Additional game-specific models (if needed)
  │
  ├── sdk/                  # SDK for integrating the service into other apps
  │   ├── __init__.py
  │   ├── core.py
  │   ├── game_processors.py
  │   ├── api_client.py
  │   ├── utils.py
  │   ├── config.py
  │   ├── exceptions.py
  │   ├── background_tasks.py
  │   ├── scheduler.py
  │   ├── versioning.py
  │   ├── logger.py
  │   ├── caching.py
  │   └── auth.py
  │
  ├── tests/                # Unit tests for validation and processors
  │   ├── model_tests/
  │   │   ├── eight_ball.py
  │   │   ├── test_chess.py
  │   ├── test_data_processing.py
  │   ├── test_db_utils.py
  │   ├── test_main.py
  │   ├── test_sdk_core.py
  │   ├── test_sdk_api_client.py
  │   └── ... (additional tests)
  │
  ├── utils/                # Utility files and common functions
  │   ├── processors/       # Game-specific processors
  │   │   ├── eight_ball_processor.py
  │   │   ├── chess_processor.py
  │   ├── data_processing.py
  │   ├── db_utils.py
  │   ├── logger.py
  │   └── middlewares/      # WebSocket and HTTP middlewares
  │       ├── __init__.py
  │       ├── logging_middleware.py
  │       ├── auth_middleware.py
  │       ├── rate_limit_middleware.py
  │       ├── request_validation_middleware.py
  │       └── cors_middleware.py
  │
  ├── config.py             # Global configuration file
  ├── 8ball_postgame_analysis.py  # Post-game summary & AI processing updates
  ├── 8ball_spectator_mode.py     # Spectator mode: AI observes before unlocking gameplay
  ├── 8ball_training.py     # Reinforcement learning training script for 8-ball
  ├── 8ball_ws_server.py    # Flask WebSocket server for real-time shot trajectory processing
  ├── main.py               # Flask API entry point
  ├── README.md             # Project documentation (this file)
  ├── requirements.txt      # Python dependencies
  ├── testdata.json         # Sample test data
  └── .env                  # Environment variables
```

---

## Setup Guide

### 1. Prerequisites

Ensure you have the following installed:

- Python 3.9 or later
- pip (Python package manager)
- A running MongoDB instance (local or cloud-based, e.g., MongoDB Atlas)

### 2. Clone the Repository

```bash
git clone https://github.com/your-repo/AI-Agent-Service.git
cd AI-Agent-Service
```

### 3. Create a Virtual Environment

It’s recommended to use a virtual environment to manage dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

Create a `.env` file in the root directory and add the following:

```env
MONGODB_URI=mongodb://localhost:27017/
FLASK_PORT=5000
SECRET_KEY=your-secret-key
```

### 6. Start the Server

Run the Flask application:

```bash
python main.py
```

The server will start at `http://localhost:5000` by default.

---

## API Documentation

### Endpoint: `/process-game-data`

- **Method**: `POST`
- **Description**: Processes and stores game data.
- **Request Body**:
  - `game` (string): The game type (e.g., "8ball", "chess").
  - `data` (object): The raw game data specific to the game.

#### Example Request:

```json
{
  "game": "8ball",
  "data": {
    "players": [
      {
        "username": "player1",
        "rating": 1000,
        "games": 10,
        "games_won": 5,
        "games_lost": 5,
        "balls_potted": 50,
        "fouls": 2,
        "game_data": [
          {
            "timestamp": 1737678409,
            "cue_ball_position": [21, 302],
            "power": 30.5,
            "angle": 45.0
          }
        ]
      }
    ]
  }
}
```

#### Example Response:

```json
{
  "message": "Data processed and stored successfully"
}
```

---

## Adding Support for a New Game

1. **Create a New Model**:

   - Add a file under `models/` to define the schema for the new game using Pydantic.

2. **Create a Processor**:

   - Add a file under `utils/processors/` to handle game-specific processing logic.

3. **Update the Processor Router**:

   - Update `utils/data_processing.py` to include the new game processor in the `get_processor` function.

4. **Write Tests**:

   - Add validation tests under `tests/model_tests/`.
   - Add processing tests under `tests/`.

5. **Test the Integration**:
   - Run all tests using `unittest`.

---

## Testing

### Run All Tests

To execute the test suite, run:

```bash
python -m unittest discover -s tests
```

---

## Extensibility

- **Game Models**: Add Pydantic models for new games in the `models/` directory.
- **Processors**: Implement game-specific logic in `utils/processors/`.
- **Database**: Each game can have its own MongoDB collection for clean data separation.

---

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
