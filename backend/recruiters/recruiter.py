from abc import ABC, abstractmethod
from typing import Literal

import pandas as pd


class Recruiter(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def output_type(self) -> Literal['categorical', 'continuous']:
        pass

    @abstractmethod
    def train(self, application_train: pd.DataFrame, score_train: pd.Series):
        pass

    @abstractmethod
    def predict_scores(self, applications: pd.DataFrame) -> pd.Series:
        pass
