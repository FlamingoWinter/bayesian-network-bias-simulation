from typing import Tuple, List

import pandas as pd
from sklearn.model_selection import train_test_split

from backend.network.bayesian_network import BayesianNetwork


class Applicants:
    def __init__(self, network: BayesianNetwork, characteristic_instances: pd.DataFrame):
        self.network: BayesianNetwork = network
        self.characteristic_instances: pd.DataFrame = characteristic_instances

    def get_applications(self, one_hot_encode_categorical_variables=False) -> pd.DataFrame:
        df = self.characteristic_instances[self.network.application_characteristics]
        if one_hot_encode_categorical_variables:
            categorical_columns = [column_name for column_name, characteristic
                                   in self.network.characteristics.items()
                                   if characteristic.type == "categorical" and column_name in df.columns]
            df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)
        return df.reset_index(drop=True)

    def get_scores(self) -> pd.Series:
        return self.characteristic_instances[self.network.score_characteristic].reset_index(drop=True)

    def characteristic_name_to_distribution(self, characteristic: str) -> List[float]:
        return self.characteristic_instances[characteristic].to_list()

    def random_split(self, split_sizes: List[float]) -> Tuple['Applicants', ...]:
        remaining = self.characteristic_instances
        splits: List[pd.DataFrame] = []
        remaining_applicants_proportion = 1
        for split_size in split_sizes[:-1]:
            test_size = 1 - (split_size / remaining_applicants_proportion)
            remaining, characteristic_split = train_test_split(remaining, test_size=test_size)
            remaining_applicants_proportion -= split_size
            splits.append(characteristic_split)
        splits.append(remaining)

        return tuple(Applicants(self.network, split) for split in splits)
