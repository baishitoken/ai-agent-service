# BAISHI AI AGENT DATA PROCESSOR SERVICE

## Introduction

BAISHI AI AGENT DATA PROCESSOR SERVICE is a modular, scalable service designed to process game data for various games such as 8-ball pool, chess, and others. The service ingests raw game data, processes it to extract insights, and stores it in a MongoDB database for further analysis or use.

This service is built with Python and leverages Flask for the API, Pydantic for schema validation, and MongoDB for data storage. It is highly extensible, allowing developers to easily add support for new games by defining game-specific models and processors.

---

## Features

- **Game-Agnostic Architecture**: Supports multiple games with separate models and processors for each.
- **Data Validation**: Uses Pydantic models to validate incoming payloads, ensuring clean and structured data.
- **MongoDB Integration**: Processes and stores game data efficiently in a MongoDB database.
- **Logging**: Tracks important events and errors using Python's `logging` module.
- **Modular Design**: Easily extendable to add new games or customize processing logic.
- **Unit Tests**: Comprehensive test suite for key components, ensuring code quality.

---

## File Structure

```
/AI-AGENT-SERVICE
  ├── models/               # Pydantic models for games
  │   ├── eight_ball.py
  │   ├── chess.py
  ├── tests/                # Unit tests for validation and processors
  │   ├── model_tests/
  │   │   ├── eight_ball.py
  │   │   ├── test_chess.py
  │   ├── test_data_processing.py
  │   ├── test_db_utils.py
  │   ├── test_main.py
  ├── utils/                # Utility files
  │   ├── processors/       # Game-specific processors
  │   │   ├── eight_ball_processor.py
  │   │   ├── chess_processor.py
  │   ├── data_processing.py
  │   ├── db_utils.py
  │   ├── logger.py
  ├── .gitattributes
  ├── config.py             # Configuration file
  ├── main.py               # Flask API entry point
  ├── README.md             # Project documentation
  ├── requirements.txt      # Dependencies
  ├── testdata.json         # Sample test data
```

---

## Setup Guide

### 1. Prerequisites

Ensure you have the following installed:

- Python 3.9 or later
- pip (Python package manager)
- MongoDB instance (local or cloud-based, e.g., MongoDB Atlas)

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
MONGODB_URI=mongodb://localhost:27017  # Replace with your MongoDB connection string
FLASK_PORT=5000                       # Port for the Flask server
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
