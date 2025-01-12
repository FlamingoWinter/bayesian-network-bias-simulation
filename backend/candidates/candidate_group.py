from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

from backend.api.reponseTypes.distributionResponse import DistributionResponse
from backend.network.bayesian_network import BayesianNetwork


class CandidateGroup:
    def __init__(self, network: BayesianNetwork, characteristics: pd.DataFrame):
        self.network: BayesianNetwork = network
        self.characteristics: pd.DataFrame = characteristics

    def train_test_split(self, test_size: float = 0.1) -> Tuple['CandidateGroup', 'CandidateGroup']:
        train, test = train_test_split(self.characteristics, test_size=test_size)

        return CandidateGroup(self.network, train), CandidateGroup(self.network, test)

    def get_applications(self) -> pd.DataFrame:
        return self.characteristics[self.network.application_characteristics]

    def get_scores(self) -> pd.Series:
        return self.characteristics[self.network.score_characteristic]

    def characteristic_to_distribution_response(self, characteristic: str) -> DistributionResponse:
        return {
            "distribution": self.characteristics[characteristic].to_list()
        }
