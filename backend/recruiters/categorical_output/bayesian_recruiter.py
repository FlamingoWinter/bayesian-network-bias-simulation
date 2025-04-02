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
        return "Bayesian Recruiter"

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
        best_model = hc.estimate(scoring_method=BicScore(data))

        self.model = BayesianNetwork(best_model.edges())

        self.model.fit(data, estimator=MaximumLikelihoodEstimator)

    def predict_scores(self, applications: pd.DataFrame) -> pd.DataFrame:
        infer = VariableElimination(self.model)
        probabilities = [
            infer.query(variables=["score"], evidence=row.to_dict()).values
            for _, row in applications.iterrows()
        ]

        return pd.DataFrame(probabilities, columns=self.model.get_cpds("score").state_names["score"])[1]
