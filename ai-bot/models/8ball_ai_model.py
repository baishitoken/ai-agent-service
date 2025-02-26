import os
import sys
import time
import math
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

# -------------------------------------------------------------------------
# 1. Configuration
# -------------------------------------------------------------------------
class Config:
    """
    Configuration settings for the 8-ball training script.
    Adjust these values to fit your environment and dataset.
    """
    # Model hyperparameters
    INPUT_SIZE = 5    # shot_accuracy, cue_ball_x, cue_ball_y, power, angle
    HIDDEN_SIZE = 64
    HIDDEN_SIZE_2 = 32
    OUTPUT_SIZE = 1   # Predict best shot type
    
    # Training hyperparameters
    LEARNING_RATE = 0.001
    BATCH_SIZE = 32
    EPOCHS = 20
    
    # Data generation settings
    NUM_SAMPLES = 1000
    MAX_POWER = 100.0
    MAX_ANGLE = 360.0
    MAX_POSITION = 100.0  # hypothetical table coordinate range
    
    # Others
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    SEED = 42


# -------------------------------------------------------------------------
# 2. Utility Functions
# -------------------------------------------------------------------------
def set_seed(seed: int):
    """
    Set random seeds for reproducibility.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def generate_synthetic_data(num_samples: int):
    """
    Generate synthetic training data for demonstration.
    
    The input data will be:
        shot_accuracy, cue_ball_x, cue_ball_y, power, angle
    
    The label will be:
        best_shot (e.g., a numeric value representing the shot type)
    
    For demonstration, we generate random data and
    a synthetic label based on a made-up formula.
    """
    data = []
    labels = []
    for _ in range(num_samples):
        shot_accuracy = random.uniform(0.1, 1.0)
        cue_ball_x = random.uniform(-Config.MAX_POSITION, Config.MAX_POSITION)
        cue_ball_y = random.uniform(-Config.MAX_POSITION, Config.MAX_POSITION)
        power = random.uniform(0.0, Config.MAX_POWER)
        angle = random.uniform(0.0, Config.MAX_ANGLE)
        
        best_shot_value = (shot_accuracy * power / 100.0) + math.sin(math.radians(angle)) * 0.5
        # clamp
        best_shot_value = max(0.0, min(1.0, best_shot_value))
        
        data.append([shot_accuracy, cue_ball_x, cue_ball_y, power, angle])
        labels.append([best_shot_value])
    
    return np.array(data, dtype=np.float32), np.array(labels, dtype=np.float32)


# -------------------------------------------------------------------------
# 3. Custom Dataset
# -------------------------------------------------------------------------
class EightBallDataset(Dataset):
    """
    A PyTorch Dataset for 8-ball pool training data.
    """
    def __init__(self, data, labels):
        """
        data: 2D numpy array of shape (num_samples, 5)
        labels: 2D numpy array of shape (num_samples, 1)
        """
        self.data = data
        self.labels = labels
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        x = self.data[idx]
        y = self.labels[idx]
        return torch.tensor(x, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)


# -------------------------------------------------------------------------
# 4. Neural Network Model
# -------------------------------------------------------------------------
class EightBallModel(nn.Module):
    """
    A simple feed-forward neural network for predicting the best shot.
    """
    def __init__(self, input_size, hidden_size, hidden_size_2, output_size):
        super(EightBallModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size_2)
        self.fc3 = nn.Linear(hidden_size_2, output_size)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.relu(out)
        out = self.fc3(out)
        return out


# -------------------------------------------------------------------------
# 5. Training Loop
# -------------------------------------------------------------------------
def train_model(model, dataloader, criterion, optimizer, epoch):
    """
    Train the model for one epoch.
    
    model: The PyTorch model
    dataloader: DataLoader for training data
    criterion: Loss function
    optimizer: Optimizer (e.g., Adam)
    epoch: Current epoch number (for logging)
    """
    model.train()
    running_loss = 0.0
    
    for batch_idx, (inputs, targets) in enumerate(dataloader):
        inputs, targets = inputs.to(Config.DEVICE), targets.to(Config.DEVICE)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
    
    avg_loss = running_loss / len(dataloader)
    print(f"Epoch [{epoch+1}], Loss: {avg_loss:.4f}")


# -------------------------------------------------------------------------
# 6. Validation (Optional)
# -------------------------------------------------------------------------
def validate_model(model, dataloader, criterion):
    """
    Validate the model on a validation set (optional).
    
    model: The PyTorch model
    dataloader: DataLoader for validation data
    criterion: Loss function
    """
    model.eval()
    running_loss = 0.0
    
    with torch.no_grad():
        for inputs, targets in dataloader:
            inputs, targets = inputs.to(Config.DEVICE), targets.to(Config.DEVICE)
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            running_loss += loss.item()
    
    avg_loss = running_loss / len(dataloader)
    return avg_loss


# -------------------------------------------------------------------------
# 7. Main Training Script
# -------------------------------------------------------------------------
def main():
    # Set seeds for reproducibility
    set_seed(Config.SEED)
    
    # Step 1: Generate or load data
    data, labels = generate_synthetic_data(Config.NUM_SAMPLES)
    
    # Split data into train/val sets (80/20 split)
    split_idx = int(0.8 * Config.NUM_SAMPLES)
    train_data = data[:split_idx]
    train_labels = labels[:split_idx]
    val_data = data[split_idx:]
    val_labels = labels[split_idx:]
    
    # Create Dataset objects
    train_dataset = EightBallDataset(train_data, train_labels)
    val_dataset = EightBallDataset(val_data, val_labels)
    
    # Create DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=Config.BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=Config.BATCH_SIZE, shuffle=False)
    
    # Step 2: Initialize the model, loss function, and optimizer
    model = EightBallModel(
        input_size=Config.INPUT_SIZE,
        hidden_size=Config.HIDDEN_SIZE,
        hidden_size_2=Config.HIDDEN_SIZE_2,
        output_size=Config.OUTPUT_SIZE
    ).to(Config.DEVICE)
    
    criterion = nn.MSELoss()  # For a regression-like task
    optimizer = optim.Adam(model.parameters(), lr=Config.LEARNING_RATE)
    
    # Step 3: Training Loop
    print("Starting Training...")
    for epoch in range(Config.EPOCHS):
        start_time = time.time()
        
        train_model(model, train_loader, criterion, optimizer, epoch)
        
        # Optional: Validate the model
        val_loss = validate_model(model, val_loader, criterion)
        
        epoch_duration = time.time() - start_time
        print(f"Validation Loss: {val_loss:.4f} | Epoch Duration: {epoch_duration:.2f}s")
    
    # Step 4: Save the trained model
    model_save_path = "8ball_model.pth"
    torch.save(model.state_dict(), model_save_path)
    print(f"Model saved to {model_save_path}")

    # Step 5: Demonstration of usage
    # Let's pick a random sample from the validation set and predict
    sample_input = torch.tensor(val_data[0], dtype=torch.float32).unsqueeze(0).to(Config.DEVICE)
    model.eval()
    with torch.no_grad():
        prediction = model(sample_input)