import numpy as np
from sklearn.linear_model import LinearRegression
from typing import Tuple, Dict, Any

class TrendAnalyzer:
    """
    Calculates smoothed metrics and trend slopes to gauge player improvement.
    """
    def __init__(self, profile):
        self.profile = profile

    def moving_average(self, series: list, window: int = 5) -> np.ndarray:
        arr = np.array(series)
        if len(arr) < window:
            return arr
        weights = np.ones(window) / window
        return np.convolve(arr, weights, mode='valid')

    def slope_intercept(self, series: list) -> Tuple[float, float]:
        if len(series) < 2:
            return 0.0, 0.0
        X = np.arange(len(series)).reshape(-1, 1)
        y = np.array(series)
        model = LinearRegression().fit(X, y)
        return float(model.coef_[0]), float(model.intercept_)

    def analyze(self) -> Dict[str, Any]:
        acc = self.profile.data['accuracy_trend']
        fouls = self.profile.data['foul_trend']
        agg = self.profile.data['aggressiveness_trend']
        win = self.profile.data['win_trend']

        acc_slope, _ = self.slope_intercept(acc)
        fouls_slope, _ = self.slope_intercept(fouls)

        return {
            'acc_ma': self.moving_average(acc),
            'fouls_ma': self.moving_average(fouls),
            'acc_slope': acc_slope,
            'fouls_slope': fouls_slope,
            'improving': acc_slope > 0 and fouls_slope < 0
        }