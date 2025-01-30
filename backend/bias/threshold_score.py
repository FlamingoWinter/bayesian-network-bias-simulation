import pandas as pd


def threshold_score(score: pd.Series, threshold: float):
    return (score['actual_score'] > threshold).astype(int)
