import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from backend.recruiters.recruiter import Recruiter


class RandomForestRecruiter(Recruiter):
    @property
    def name(self):
        return "Random Forest Recruiter"

    @property
    def output_type(self):
        return "categorical"

    def __init__(self):
        self.model = RandomForestClassifier()

    def train(self, application_train: pd.DataFrame, score_train: pd.Series):
        self.model.fit(application_train, score_train)

    def predict_scores(self, applications: pd.DataFrame) -> pd.Series:
        predicted_scores = pd.Series(self.model.predict(applications))
        predicted_scores.index = applications.index
        return predicted_scores
