from typing import Dict

import pandas as pd

from backend.api.responseTypes.recruiterBiasAnalysisResponse.recruiterBiasAnalysisResponse import \
    RecruiterBiasAnalysisResponse
from backend.bias.categorical.categorical_recruiter_bias_analysis import CategoricalRecruiterBiasAnalysis
from backend.bias.continuous.continuous_recruiter_bias_analysis import ContinuousRecruiterBiasAnalysis
from backend.bias.threshold_score import threshold_score
from backend.candidates.candidate_group import CandidateGroup
from backend.network.bayesian_network import Characteristic
from backend.recruiters.recruiter import Recruiter
from backend.utilities.convert_logits_to_decision import convert_logits_to_decision


class RecruiterBiasAnalysis:
    def __init__(self, recruiter: Recruiter,
                 candidate_group: CandidateGroup, application_test: pd.DataFrame,
                 protected_characteristic: Characteristic, score_threshold: float = None):

        is_score_categorical: bool = candidate_group.network.characteristics[
                                         candidate_group.network.score_characteristic].type == "categorical"

        is_recruiter_categorical: bool = recruiter.output_type == "categorical"

        actual_scores = candidate_group.get_scores()

        predicted_scores = recruiter.predict_scores(application_test)
        if is_recruiter_categorical:
            proportion_hired = actual_scores.sum() / len(actual_scores)
            predicted_scores = convert_logits_to_decision(predicted_scores, proportion_hired)

        group = candidate_group.characteristics[protected_characteristic.name]

        if is_recruiter_categorical and not is_score_categorical:
            actual_scores = threshold_score(actual_scores, score_threshold)

        actual_scores.reset_index(drop=True, inplace=True)
        group.reset_index(drop=True, inplace=True)
        self.applications = pd.concat(
            [actual_scores, predicted_scores, group], axis=1)
        self.applications.columns = ['actual_score', 'predicted_score', 'group']
        self.protected_characteristic = protected_characteristic

        self.categorical_recruiter_bias_analysis = None
        self.continuous_recruiter_bias_analysis = None

        if not is_recruiter_categorical and not is_score_categorical:
            self.continuous_recruiter_bias_analysis = ContinuousRecruiterBiasAnalysis(self.applications,
                                                                                      self.protected_characteristic)

            self.applications['actual_score'] = threshold_score(self.applications['actual_score'], score_threshold)
            self.applications['predicted_score'] = threshold_score(self.applications['predicted_score'],
                                                                   score_threshold)
            self.categorical_recruiter_bias_analysis = CategoricalRecruiterBiasAnalysis(self.applications,
                                                                                        self.protected_characteristic)
        else:
            self.categorical_recruiter_bias_analysis = CategoricalRecruiterBiasAnalysis(self.applications,
                                                                                        self.protected_characteristic)

    def print_summary(self):
        if self.categorical_recruiter_bias_analysis is not None:
            self.categorical_recruiter_bias_analysis.print_summary()
        if self.continuous_recruiter_bias_analysis is not None:
            self.continuous_recruiter_bias_analysis.print_summary()

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
