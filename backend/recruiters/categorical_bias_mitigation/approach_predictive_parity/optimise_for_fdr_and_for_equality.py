import numpy as np
import pandas as pd

from backend.recruiters.categorical_bias_mitigation.mitigation import Mitigation


class OptimiseForFDRAndFOREquality(Mitigation):
    protected_characteristic_name: str

    @property
    def name(self) -> str:
        return "Optimise for FDR and FOR Equality"

    def loss(self,
             proportion_hired: np.array,
             score_holdout: pd.Series,
             predicted_holdout: pd.Series,
             groups: pd.Series) -> float:
        fnr, fpr, fdr, f_o_r, accuracy = self.get_fnr_fpr_fdr_for_acc(score_holdout, predicted_holdout, groups)

        return fdr.var() + f_o_r.var()
