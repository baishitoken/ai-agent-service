import numpy as np
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

PLAYSTYLES = ["PS_AGGRESSIVE__M", "PS_DEFENSIVE__M", "PS_CALCULATED__M"]

def generate_synthetic_8ball_data(num_samples=500):
    """
    Generate synthetic data for training the classifier.
    Features: shot power, accuracy, foul rate
    Labels: Aggressive, Defensive, Calculated
    """
    data = []
    labels = []
    
    for _ in range(num_samples):
        shot_power = random.uniform(10, 100)  # Power between 10-100
        accuracy = random.uniform(0.4, 1.0)   # Accuracy between 40%-100%
        foul_rate = random.uniform(0, 0.3)    # Fouls per game (0-30%)
        
        # Assign labels based on thresholds
        if shot_power > 75 and accuracy < 0.7:
            playstyle = "PS_AGGRESSIVE__M"  # High power, lower accuracy
        elif foul_rate > 0.2 or shot_power < 40:
            playstyle = "PS_DEFENSIVE__M"   # High fouls or very low power
        else:
            playstyle = "PS_CALCULATED__M"  # Balanced
        
        data.append([shot_power, accuracy, foul_rate])
        labels.append(playstyle)
    
    return np.array(data), np.array(labels)

def train_8ball_playstyle_classifier():
    """
    Train a RandomForestClassifier to classify players into Aggressive, Defensive, or Calculated.
    Returns the trained model and scaler.
    """
    X, y = generate_synthetic_8ball_data()

    y_encoded = np.array([PLAYSTYLES.index(label) for label in y])

    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Training Completed - Accuracy: {accuracy:.2f}")

    return model, scaler

def classify_8ball_playstyle(model, scaler, shot_power, accuracy, foul_rate):
    """
    Predict a player's dominant playstyle based on shot power, accuracy, and foul rate.
    """
    input_data = np.array([[shot_power, accuracy, foul_rate]])
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)
    return PLAYSTYLES[prediction[0]]

trained_model, trained_scaler = train_8ball_playstyle_classifier()