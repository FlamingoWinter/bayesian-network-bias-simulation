import numpy as np
import pandas as pd


def convert_logits_to_decisions(predicted_score_logits: pd.Series, proportion_hired: float) -> pd.Series:
    threshold = predicted_score_logits.quantile(1 - proportion_hired)
    num_selected = int(len(predicted_score_logits) * proportion_hired)

    above_threshold = predicted_score_logits > threshold
    equal_threshold = predicted_score_logits == threshold

    remaining_needed = num_selected - above_threshold.sum()
    if remaining_needed > 0:
        equal_indices = predicted_score_logits[equal_threshold].index
        drop_indices = np.random.choice(equal_indices, len(equal_indices) - remaining_needed, replace=False)
        equal_threshold.loc[drop_indices] = False

    return (above_threshold | equal_threshold).astype(int)
