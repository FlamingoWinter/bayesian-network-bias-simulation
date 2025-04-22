import numpy as np
import pandas as pd

from backend.recruiters.categorical_bias_mitigation.mitigation import Mitigation


class OptimiseForFNRFPRAccuracy(Mitigation):
    protected_characteristic_name: str

    @property
    def name(self) -> str:
        return "Optimise for FNR and FPR Equality, and Accuracy"

    def loss(self,
             proportion_hired: np.array,
             score_holdout: pd.Series,
             predicted_holdout: pd.Series,
             groups: pd.Series) -> float:
        fnr, fpr, fdr, f_o_r, accuracy = self.get_fnr_fpr_fdr_for_acc(score_holdout, predicted_holdout, groups)

        return fpr.var() + fnr.var() + (1 - accuracy) ** 2
