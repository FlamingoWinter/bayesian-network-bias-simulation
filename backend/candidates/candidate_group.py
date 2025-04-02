from typing import Tuple, List

import pandas as pd
from sklearn.model_selection import train_test_split

from backend.network.bayesian_network import BayesianNetwork


class CandidateGroup:
    def __init__(self, network: BayesianNetwork, characteristics: pd.DataFrame):
        self.network: BayesianNetwork = network
        self.characteristics: pd.DataFrame = characteristics

    def random_split(self, split_sizes: List[float]) -> Tuple['CandidateGroup', ...]:
        remaining = self.characteristics
        characteristic_splits: List[pd.DataFrame] = []
        split_size_left = 1
        for size in split_sizes[:-1]:
            remaining, characteristic_split = train_test_split(remaining, test_size=1 - (size / split_size_left))
            split_size_left -= size
            characteristic_splits.append(characteristic_split)
        characteristic_splits.append(remaining)

        return tuple(CandidateGroup(self.network, split) for split in characteristic_splits)

    def get_applications(self, one_hot_encode_categorical_variables=False) -> pd.DataFrame:
        df = self.characteristics[self.network.application_characteristics]
        if one_hot_encode_categorical_variables:
            categorical_columns = [column_name for column_name, characteristic
                                   in self.network.characteristics.items()
                                   if characteristic.type == "categorical" and column_name in df.columns]
            df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)
        return df.reset_index(drop=True)

    def get_scores(self) -> pd.Series:
        return self.characteristics[self.network.score_characteristic].reset_index(drop=True)

    def characteristic_to_distribution(self, characteristic: str) -> List[float]:
        return self.characteristics[characteristic].to_list()
