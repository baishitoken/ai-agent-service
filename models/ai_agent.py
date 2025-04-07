import logging
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
import numpy as np
import random
from collections import deque
from typing import Deque, Tuple, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DuelingDQNAgent:
    """
    A DQN agent with dueling architecture and optional prioritized replay.
    """
    def __init__(
        self,
        state_size: int,
        action_size: int,
        learning_rate: float = 0.001,
        gamma: float = 0.95,
        epsilon: float = 1.0,
        epsilon_min: float = 0.01,
        epsilon_decay: float = 0.995,
        memory_size: int = 50000,
        batch_size: int = 64,
        use_per: bool = False
    ):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.memory: Deque[Tuple[np.ndarray, int, float, np.ndarray, bool]] = deque(maxlen=memory_size)
        self.batch_size = batch_size
        self.use_per = use_per

        # Main and target networks
        self.model = self._build_dueling_model()
        self.target_model = self._build_dueling_model()
        self.update_target_model()

    def _build_dueling_model(self) -> models.Model:
        inputs = layers.Input(shape=(self.state_size,))
        x = layers.Dense(256, activation='relu')(inputs)
        x = layers.Dense(256, activation='relu')(x)

        # Value stream
        value = layers.Dense(128, activation='relu')(x)
        value = layers.Dense(1, activation='linear')(value)

        # Advantage stream
        adv = layers.Dense(128, activation='relu')(x)
        adv = layers.Dense(self.action_size, activation='linear')(adv)

        # Combine streams
        adv_mean = layers.Lambda(lambda a: tf.reduce_mean(a, axis=1, keepdims=True))(adv)
        q_vals = layers.Add()([value, layers.Subtract()([adv, adv_mean])])

        model = models.Model(inputs=inputs, outputs=q_vals)
        model.compile(
            optimizer=optimizers.Adam(learning_rate=self.learning_rate),
            loss='huber'
        )
        return model

    def update_target_model(self) -> None:
        self.target_model.set_weights(self.model.get_weights())
        logger.debug("Target model updated")

    def remember(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool) -> None:
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state: np.ndarray, explore: bool = True) -> int:
        if explore and np.random.rand() < self.epsilon:
            choice = random.randrange(self.action_size)
            logger.debug("Random action: %d", choice)
            return choice
        q = self.model.predict(state[np.newaxis, :], verbose=0)[0]
        return int(np.argmax(q))

    def replay(self) -> None:
        if len(self.memory) < self.batch_size:
            return
        minibatch = random.sample(self.memory, self.batch_size)

        states = np.vstack([m[0] for m in minibatch])
        next_states = np.vstack([m[3] for m in minibatch])

        q_next = self.target_model.predict(next_states, verbose=0)
        q_current = self.model.predict(states, verbose=0)

        for i, (state, action, reward, next_state, done) in enumerate(minibatch):
            target = q_current[i]
            target_val = reward if done else reward + self.gamma * np.max(q_next[i])
            target[action] = target_val
            q_current[i] = target

        self.model.fit(
            states,
            q_current,
            batch_size=self.batch_size,
            epochs=1,
            verbose=0
        )

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save(self, path: str) -> None:
        self.model.save_weights(path)
        logger.info("Model weights saved to %s", path)

    def load(self, path: str) -> None:
        self.model.load_weights(path)
        self.update_target_model()
        logger.info("Model weights loaded from %s", path)