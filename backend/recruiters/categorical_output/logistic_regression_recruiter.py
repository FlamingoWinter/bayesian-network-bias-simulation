from typing import List

import pandas as pd
from sklearn.linear_model import LogisticRegression

from backend.recruiters.categorical_bias_mitigation.mitigation import Mitigation
from backend.recruiters.recruiter import Recruiter


class LogisticRegressionRecruiter(Recruiter):
    @property
    def name(self):
        return "Logistic Regression"

    @property
    def output_type(self):
        return "categorical"

    def __init__(self, mitigations: List[Mitigation]):
        super().__init__(mitigations)
        self.model = LogisticRegression()

    def train(self, application_train: pd.DataFrame, score_train: pd.Series):
        self.model.fit(application_train, score_train)

    def predict_scores(self, applications: pd.DataFrame) -> pd.Series:
        predicted_scores = pd.Series(self.model.decision_function(applications))
        return predicted_scores
