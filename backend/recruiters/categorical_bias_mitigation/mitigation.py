import warnings
from abc import ABC, abstractmethod
from typing import Callable

import numpy as np
import pandas as pd
from scipy.optimize import dual_annealing

from backend.utilities.time_function import time_function


class Mitigation(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def extract_hiring_proportions_from_training_and_holdout(self, score_train: pd.Series, groups_train: pd.Series,
                                                             score_holdout: pd.Series,
                                                             predicted_holdout: pd.Series,
                                                             groups_holdout: pd.Series):
        pass

    @staticmethod
    def threshold_scores(scores: pd.Series, proportion_hired: float, randomise=True) -> pd.Series:
        if np.isnan(proportion_hired):
            proportion_hired = 0
        proportion_hired = np.clip(proportion_hired, 0.01, 0.99)
        threshold = scores.quantile(1 - proportion_hired)
        num_selected = int(len(scores) * proportion_hired)

        above_threshold = (scores > threshold)
        equal_threshold = scores == threshold

        remaining_needed = num_selected - above_threshold.sum()
        if remaining_needed > 0:
            equal_indices = scores[equal_threshold].index
            if randomise and len(equal_indices) > 0:
                drop_indices = np.random.choice(equal_indices, len(equal_indices) - remaining_needed, replace=False)
                equal_threshold.loc[drop_indices] = False
            else:
                equal_indices = scores[equal_threshold].index[:remaining_needed]
                equal_threshold.loc[~equal_threshold.index.isin(equal_indices)] = False

        return (above_threshold | equal_threshold).astype(int)

    @staticmethod
    @time_function("Minimising Loss")
    def get_proportions_to_minimise_loss(
            total_proportion_hired: float,
            score_holdout: pd.Series,
            predicted_holdout: pd.Series,
            groups_holdout: pd.Series,
            loss: Callable[[np.array, pd.Series, pd.Series, pd.Series], float]
            # proportion_hired, score_holdout, predicted_holdout, groups
    ):
        def loss_function(proportion_hired_partial):
            last_value = (total_proportion_hired - np.sum(proportion_hired_partial * group_proportions[:-1])
                          ) / group_proportions.iloc[-1]

            proportion_hired = np.append(proportion_hired_partial, last_value)

            if np.any(proportion_hired < 0) or np.any(proportion_hired > 1):
                return np.inf

            return loss(proportion_hired, score_holdout, predicted_holdout, groups_holdout)

        group_proportions = groups_holdout.value_counts(normalize=True).sort_index()

        warnings.simplefilter("ignore", category=RuntimeWarning)

        proportion_hired_partial = dual_annealing(
            loss_function,
            bounds=[(0, 1)] * (len(group_proportions) - 1),
            maxiter=200,
        ).x

        warnings.simplefilter("default", category=RuntimeWarning)

        last_value = (total_proportion_hired - np.sum(proportion_hired_partial * group_proportions[:-1])
                      ) / group_proportions.iloc[-1]

        print("solution found", np.append(proportion_hired_partial, last_value))
        print("creates loss", loss_function(proportion_hired_partial))

        return np.append(proportion_hired_partial, last_value)

    @abstractmethod
    def convert_scores_to_decisions(self, predicted_score: pd.Series, groups: pd.Series) -> pd.Series:
        pass
