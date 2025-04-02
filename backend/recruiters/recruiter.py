from abc import ABC, abstractmethod
from typing import Literal, List

import pandas as pd

from backend.recruiters.categorical_bias_mitigation.mitigation import Mitigation


class Recruiter(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def output_type(self) -> Literal['categorical', 'continuous']:
        pass

    def __init__(self, mitigations: List[Mitigation]):
        self.mitigations = mitigations

    def initalise_mitigation(self,
                             score_train: pd.Series, groups_train: pd.Series,
                             score_holdout: pd.Series, application_holdout: pd.DataFrame, groups_holdout: pd.Series):
        predicted_holdout = self.predict_scores(application_holdout)
        for mitigation in self.mitigations:
            mitigation.extract_hiring_proportions_from_training_and_holdout(
                score_train, groups_train,
                score_holdout.reset_index(drop=True), predicted_holdout, groups_holdout.reset_index(drop=True))

    @abstractmethod
    def train(self, application_train: pd.DataFrame, score_train: pd.Series):
        pass

    @abstractmethod
    def predict_scores(self, applications: pd.DataFrame) -> pd.Series:
        pass

    def predict_decisions_for_each_mitigation(self, applications: pd.DataFrame, groups: pd.Series) -> dict[
        str, pd.Series]:
        scores = self.predict_scores(applications)
        decisions = {}
        for mitigation in self.mitigations:
            decisions[mitigation.name] = mitigation.convert_scores_to_decisions(scores, groups)
        return decisions
