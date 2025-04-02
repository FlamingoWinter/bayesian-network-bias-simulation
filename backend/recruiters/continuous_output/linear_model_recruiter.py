import pandas as pd
from sklearn.linear_model import LinearRegression

from backend.recruiters.categorical_bias_mitigation.mitigation import Mitigation
from backend.recruiters.recruiter import Recruiter


class LinearModelRecruiter(Recruiter):
    @property
    def name(self):
        return "Linear Model Recruiter"

    @property
    def output_type(self):
        return "continuous"

    def __init__(self, mitigation: Mitigation):
        super().__init__(mitigation)
        self.model = LinearRegression()

    def train(self, application_train: pd.DataFrame, score_train: pd.Series):
        self.model.fit(application_train, score_train)

    def predict_scores(self, applications: pd.DataFrame) -> pd.Series:
        predicted_scores = pd.Series(self.model.predict(applications))
        predicted_scores.index = applications.index
        return predicted_scores
