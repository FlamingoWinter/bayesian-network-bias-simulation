from typing import Dict

import pandas as pd

from backend.api.responseTypes.recruiterBiasAnalysisResponse.recruiterBiasAnalysisResponse import \
    RecruiterBiasAnalysisResponse
from backend.bias.mitigation_bias_analysis import MitigationBiasAnalysis
from backend.candidates.candidate_group import CandidateGroup
from backend.network.bayesian_network import Characteristic
from backend.recruiters.recruiter import Recruiter


class RecruiterBiasAnalysis:
    def __init__(self, recruiter: Recruiter,
                 candidate_group: CandidateGroup, application_test: pd.DataFrame,
                 protected_characteristic: Characteristic):
        self.recruiter = recruiter

        actual_scores = candidate_group.get_scores()

        groups = candidate_group.characteristics[protected_characteristic.name]

        groups.reset_index(drop=True, inplace=True)
        actual_scores.reset_index(drop=True, inplace=True)

        predicted_scores_for_each_mitigation = recruiter.predict_decisions_for_each_mitigation(application_test, groups)

        self.analysis_by_mitigation = {}
        for mitigation_name, predicted_scores in predicted_scores_for_each_mitigation.items():
            applications = pd.concat(
                [actual_scores, predicted_scores, groups], axis=1)
            applications.columns = ['actual_score', 'predicted_score', 'group']

            self.analysis_by_mitigation[mitigation_name] = MitigationBiasAnalysis(applications,
                                                                                  protected_characteristic)

    def print_summary(self):
        for mitigation_name, mitigation_bias_analysis in self.analysis_by_mitigation.items():
            print("\nMitigation: ", mitigation_name)
            mitigation_bias_analysis.print_summary()

    # TODO
    def to_response(self) -> RecruiterBiasAnalysisResponse:
        return {mitigation: bias_analysis.to_response() for mitigation, bias_analysis in
                self.analysis_by_mitigation.items()}


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
