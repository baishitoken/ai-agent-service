import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

def build_model(input_shape, action_space):
    """Build a deep neural network for reinforcement learning."""
    model = models.Sequential([
        # Input Layer
        layers.InputLayer(input_shape=input_shape),
        # Hidden layers
        layers.Dense(256, activation='relu'),   # First hidden layer with ReLU activation
        layers.Dense(128, activation='relu'),   # Second hidden layer
        layers.Dense(64, activation='relu'),    # Third hidden layer
        # Output Layer
        layers.Dense(action_space, activation='linear')  # Action space (e.g., shot types or actions)
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), loss='mean_squared_error')
    return model

def predict_action(model, state):
    """Predict the next action based on the current state."""
    state = np.array(state).reshape(1, -1)  # Reshape state to match the model input shape
    action_probs = model(state)             # Predict action probabilities
    action = np.argmax(action_probs, axis=-1)  # Choose the action with the highest probability
    return action

def train_model(model, states, actions, rewards, next_states, gamma=0.99):
    """Train the model using the Bellman equation (Q-learning)."""
    # Calculate the future rewards (discounted)
    future_rewards = model.predict(next_states)
    max_future_rewards = np.max(future_rewards, axis=1)  # Best possible future reward

    target_q_values = rewards + (gamma * max_future_rewards)

    # Train on the target Q-values
    with tf.GradientTape() as tape:
        q_values = model(states)
        # Gather Q-values for the taken actions
        action_q_values = tf.gather(q_values, actions, axis=1, batch_dims=1)
        loss = tf.reduce_mean(tf.square(target_q_values - action_q_values))  # MSE loss

    grads = tape.gradient(loss, model.trainable_variables)
    model.optimizer.apply_gradients(zip(grads, model.trainable_variables))

    return loss
