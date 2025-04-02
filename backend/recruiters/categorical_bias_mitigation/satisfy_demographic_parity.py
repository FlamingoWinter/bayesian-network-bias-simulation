import pandas as pd

from backend.recruiters.categorical_bias_mitigation.mitigation import Mitigation


class SatisfyDemographicParity(Mitigation):
    proportion_hired: float

    def name(self) -> str:
        return "Ensure Demographic Parity"

    def convert_scores_to_decisions(self, predicted_score: pd.Series, groups: pd.Series) -> pd.Series:
        decisions = pd.Series(0, index=predicted_score.index)

        for group, group_scores in predicted_score.groupby(groups):
            decisions.loc[group_scores.index] = self.threshold_scores(group_scores, self.proportion_hired)

        return decisions

    def extract_hiring_proportions_from_training_and_holdout(self, score_train: pd.Series, groups_train: pd.Series,
                                                             score_holdout: pd.Series,
                                                             predicted_holdout: pd.Series,
                                                             groups_holdout: pd.Series):
        self.proportion_hired = score_train.sum() / len(score_train)
