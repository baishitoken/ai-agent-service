from ai_model import predict_action
from ai_config import AIConfig

def predict_shot_accuracy(model, state):
    """Predict the shot accuracy based on the current state."""
    action = predict_action(model, state)
    # Convert action to shot accuracy or other metrics here
    accuracy = AIConfig.SHOT_ACCURACY[action]
    return accuracy
