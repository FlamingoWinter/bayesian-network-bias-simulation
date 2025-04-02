import pandas as pd

from backend.api.responseTypes.recruiterBiasAnalysisResponse.recruiterBiasAnalysisResponse import \
    RecruiterBiasAnalysisResponse
from backend.bias.categorical.categorical_recruiter_bias_analysis import CategoricalRecruiterBiasAnalysis
from backend.network.bayesian_network import Characteristic


class MitigationBiasAnalysis:
    def __init__(self, actual_scores: pd.Series, predicted_scores: pd.Series, groups: pd.Series,
                 protected_characteristic: Characteristic):
        self.applications = pd.concat(
            [actual_scores, predicted_scores, groups], axis=1)
        self.applications.columns = ['actual_score', 'predicted_score', 'group']
        self.protected_characteristic = protected_characteristic

        self.categorical_recruiter_bias_analysis = None
        self.continuous_recruiter_bias_analysis = None

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
