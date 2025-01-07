from abc import ABC, abstractmethod

import pandas as pd


class Recruiter(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def train(self, application_train: pd.DataFrame, score_train: pd.Series):
        pass

    @abstractmethod
    def predict_scores(self, applications: pd.DataFrame) -> pd.Series:
        pass
