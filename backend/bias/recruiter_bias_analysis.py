from typing import Dict

import pandas as pd

from backend.api.responseTypes.recruiterBiasAnalysisResponse.recruiterBiasAnalysisResponse import \
    RecruiterBiasAnalysisResponse
from backend.bias.mitigation_bias_analysis import MitigationBiasAnalysis
from backend.bias.threshold_score import threshold_score
from backend.candidates.candidate_group import CandidateGroup
from backend.network.bayesian_network import Characteristic
from backend.recruiters.recruiter import Recruiter


class RecruiterBiasAnalysis:
    def __init__(self, recruiter: Recruiter,
                 candidate_group: CandidateGroup, application_test: pd.DataFrame,
                 protected_characteristic: Characteristic, score_threshold: float = None):

        is_score_categorical: bool = candidate_group.network.characteristics[
                                         candidate_group.network.score_characteristic].type == "categorical"

        is_recruiter_categorical: bool = recruiter.output_type == "categorical"

        actual_scores = candidate_group.get_scores()
        if is_recruiter_categorical and not is_score_categorical:
            actual_scores = threshold_score(actual_scores, score_threshold)

        groups = candidate_group.characteristics[protected_characteristic.name]

        groups.reset_index(drop=True, inplace=True)
        actual_scores.reset_index(drop=True, inplace=True)

        predicted_scores_for_each_mitigation = recruiter.predict_decisions_for_each_mitigation(application_test, groups)

        self.analysis_by_mitigation = {}
        for mitigation_name, predicted_scores in predicted_scores_for_each_mitigation.items():
            self.analysis_by_mitigation[mitigation_name] = MitigationBiasAnalysis(actual_scores, predicted_scores,
                                                                                  groups, protected_characteristic)

    def print_summary(self):
        for mitigation_name, mitigation_bias_analysis in self.analysis_by_mitigation.items():
            print("\nMitigation: ", mitigation_name)
            mitigation_bias_analysis.print_summary()

    def to_response(self) -> RecruiterBiasAnalysisResponse:
        return {
            "categoricalBiasAnalysis": None if self.categorical_recruiter_bias_analysis is None else self.categorical_recruiter_bias_analysis.to_response(),
            "continuousBiasAnalysis": None if self.continuous_recruiter_bias_analysis is None else self.continuous_recruiter_bias_analysis.to_response(),
        }


def print_bias_summary(bias_by_recruiter: Dict[Recruiter, RecruiterBiasAnalysis]) -> None:
    # TODO - Implement this function correctly
    print("-----------------------")
    print("Bias Summary")
    print("-----------------------")

    for recruiter, recruiter_bias_measurement in bias_by_recruiter.items():
        print(f"{recruiter.name}:")
        recruiter_bias_measurement.print_summary()
        print(
            f"----------------------------------------------------------------------------------------------------------------------------------------")
    pass

    print("")
