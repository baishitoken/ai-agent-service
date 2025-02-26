import numpy as np
import random
from ai_model import build_model, train_model, predict_action
from ai_config import AIConfig
from utils.logger import logger

class ReinforcementLearningAgent:
    def __init__(self, input_shape, action_space):
        """Initialize the RL agent with the given input shape and action space."""
        self.model = build_model(input_shape, action_space)
        self.epsilon = AIConfig.EXPLORATION_RATE  # Exploration vs Exploitation
        self.gamma = AIConfig.DISCOUNT_FACTOR     # Future rewards discount factor
        self.learning_rate = AIConfig.LEARNING_RATE
        self.memory = []  # Store agent's experiences

    def observe(self, state, action, reward, next_state):
        """Store the agent's experiences (state, action, reward, next state)."""
        self.memory.append((state, action, reward, next_state))

    def train(self):
        """Train the agent using stored experiences."""
        if len(self.memory) < AIConfig.BATCH_SIZE:
            return
        batch = random.sample(self.memory, AIConfig.BATCH_SIZE)
        states, actions, rewards, next_states = zip(*batch)

        # Convert to numpy arrays for model compatibility
        states = np.array(states)
        actions = np.array(actions)
        rewards = np.array(rewards)
        next_states = np.array(next_states)

        # Train the model using Q-learning
        loss = train_model(self.model, states, actions, rewards, next_states, self.gamma)

        logger.info(f"Training step completed with loss: {loss.numpy()}")

    def act(self, state):
        """Choose an action based on epsilon-greedy strategy."""
        if random.random() < self.epsilon:  # Exploration
            return random.randint(0, AIConfig.ACTION_SPACE - 1)  # Random action
        else:  # Exploitation
            return predict_action(self.model, state)  # Predicted action
