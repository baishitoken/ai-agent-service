class AIConfig:
    """AI configuration for the RL model and training parameters."""
    # Training parameters
    EXPLORATION_RATE = 0.1  # 10% exploration, 90% exploitation
    DISCOUNT_FACTOR = 0.99  # Discount factor for future rewards
    LEARNING_RATE = 0.001   # Learning rate for the optimizer
    BATCH_SIZE = 32         # Batch size for training
    ACTION_SPACE = 10       # Number of possible actions (e.g., different shot types)

    # Shot accuracy predictions (this could be based on the predicted action)
    SHOT_ACCURACY = [0.5, 0.7, 0.6, 0.8, 0.9, 0.95, 0.85, 0.6, 0.75, 0.65]

    # MongoDB configuration (ensure you have MongoDB running)
    MONGODB_URI = "mongodb://localhost:27017/"
    DATABASE_NAME = "game_database"
