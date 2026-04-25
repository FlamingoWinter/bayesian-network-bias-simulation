from typing import List

import pandas as pd
from pgmpy.estimators import MaximumLikelihoodEstimator, HillClimbSearch, BicScore
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork

from backend.recruiters.categorical_bias_mitigation.mitigation import Mitigation
from backend.recruiters.recruiter import Recruiter


class BayesianRecruiter(Recruiter):
    @property
    def name(self):
        return "Bayesian"

    @property
    def output_type(self):
        return "categorical"

    def __init__(self, mitigations: List[Mitigation]):
        super().__init__(mitigations)
        self.model = BayesianNetwork()

    def train(self, application_train: pd.DataFrame, score_train: pd.Series):
        data = application_train.copy()
        data["score"] = score_train

        hc = HillClimbSearch(data)
        best_model = hc.estimate(scoring_method=BicScore(data))  # type: ignore

        self.model = BayesianNetwork(best_model.edges())

        self.model.fit(data, estimator=MaximumLikelihoodEstimator)

    def predict_scores(self, applications: pd.DataFrame) -> pd.Series:
        infer = VariableElimination(self.model)
        probabilities = [
            infer.query(variables=["score"], evidence=row.to_dict()).values  # type: ignore
            for _, row in applications.iterrows()
        ]

        cpd = self.model.get_cpds("score")
        state_names = cpd.state_names["score"] if cpd is not None else None  # type: ignore
        return pd.DataFrame(probabilities, columns=state_names)[1]  # type: ignore
