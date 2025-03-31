from typing import Tuple, List

import pandas as pd
from sklearn.model_selection import train_test_split

from backend.network.bayesian_network import BayesianNetwork


class CandidateGroup:
    def __init__(self, network: BayesianNetwork, characteristics: pd.DataFrame):
        self.network: BayesianNetwork = network
        self.characteristics: pd.DataFrame = characteristics

    def train_test_split(self, train_size: float = 0.9) -> Tuple['CandidateGroup', 'CandidateGroup']:
        train, test = train_test_split(self.characteristics, test_size=1 - train_size)

        return CandidateGroup(self.network, train), CandidateGroup(self.network, test)

    def get_applications(self, one_hot_encode_categorical_variables=False) -> pd.DataFrame:
        df = self.characteristics[self.network.application_characteristics]
        if one_hot_encode_categorical_variables:
            categorical_columns = [column_name for column_name, characteristic
                                   in self.network.characteristics.items()
                                   if characteristic.type == "categorical" and column_name in df.columns]
            df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)
        return df

    def get_scores(self) -> pd.Series:
        return self.characteristics[self.network.score_characteristic]

    def characteristic_to_distribution(self, characteristic: str) -> List[float]:
        return self.characteristics[characteristic].to_list()
