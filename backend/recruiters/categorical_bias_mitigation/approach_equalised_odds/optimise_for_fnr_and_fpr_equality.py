import numpy as np
import pandas as pd

from backend.recruiters.categorical_bias_mitigation.mitigation import Mitigation


class OptimiseForFNRAndFPREquality(Mitigation):
    proportion_hireds: np.array
    protected_characteristic_name: str

    def name(self) -> str:
        return "Optimise for FNR and FPR Equality"

    def predictions_and_proportion_hired_to_decisions(self, prediction: pd.Series, groups: pd.Series,
                                                      proportion_hireds: np.array):
        decisions = pd.Series(0, index=prediction.index)

        group_order = sorted(groups.unique())
        grouped = prediction.groupby(groups)

        for i, group in enumerate(group_order):
            group_scores = grouped.get_group(group)
            decisions.loc[group_scores.index] = self.threshold_scores(group_scores, proportion_hireds[i])

        return decisions

    def convert_scores_to_decisions(self, predicted_score: pd.Series, groups: pd.Series) -> pd.Series:
        return self.predictions_and_proportion_hired_to_decisions(predicted_score, groups, self.proportion_hireds)

    def calculate_fnr_and_fpr_variance(self,
                                       proportion_hired: np.array,
                                       score_holdout: pd.Series,
                                       predicted_holdout: pd.Series,
                                       groups: pd.Series) -> float:
        decisions = self.predictions_and_proportion_hired_to_decisions(predicted_holdout, groups, proportion_hired)
        false_positives = ((score_holdout == 0) & (decisions == 1)).groupby(groups).sum().sort_index()
        not_competent = (score_holdout == 0).groupby(groups).sum().sort_index()
        fpr = false_positives / not_competent

        false_negatives = ((score_holdout == 1) & (decisions == 0)).groupby(groups).sum().sort_index()
        competent = (score_holdout == 1).groupby(groups).sum().sort_index()
        fnr = false_negatives / competent

        return fpr.var() + fnr.var()

    def extract_hiring_proportions_from_training_and_holdout(self, score_train: pd.Series, groups_train: pd.Series,
                                                             score_holdout: pd.Series,
                                                             predicted_holdout: pd.Series,
                                                             groups_holdout: pd.Series):
        total_proportion_hired = score_train.sum() / len(score_train)

        self.proportion_hireds = self.get_proportions_to_minimise_loss(
            total_proportion_hired, score_holdout, predicted_holdout, groups_holdout,
            self.calculate_fnr_and_fpr_variance)
