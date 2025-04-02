import pandas as pd

from backend.recruiters.categorical_bias_mitigation.mitigation import Mitigation


class NoMitigation(Mitigation):
    proportion_hired: float

    def name(self) -> str:
        return "No Mitigation"

    def convert_scores_to_decisions(self, predicted_score: pd.Series, groups: pd.Series) -> pd.Series:
        return self.threshold_scores(predicted_score, self.proportion_hired)

    def extract_hiring_proportions_from_training_and_holdout(self, score_train: pd.Series, groups_train: pd.Series,
                                                             score_holdout: pd.Series,
                                                             predicted_holdout: pd.Series,
                                                             groups_holdout: pd.Series):
        self.proportion_hired = score_train.sum() / len(score_train)
