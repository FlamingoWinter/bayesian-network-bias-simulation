from typing import List

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from backend.simulation.train_recruiters.mitigation.base import Mitigation
from backend.simulation.train_recruiters.recruiter import Recruiter


class RandomForestRecruiter(Recruiter):
    @property
    def name(self):
        return "Random Forest"

    @property
    def output_type(self):
        return "categorical"

    def __init__(self, mitigations: List[Mitigation]):
        super().__init__(mitigations)
        self.model = RandomForestClassifier()

    def train(self, application_train: pd.DataFrame, score_train: pd.Series):
        self.model.fit(application_train, score_train)

    def predict_scores(self, applications: pd.DataFrame) -> pd.Series:
        predicted_scores = pd.Series(self.model.predict_proba(applications)[:, 1])  # type: ignore
        return predicted_scores
