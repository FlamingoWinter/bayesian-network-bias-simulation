from typing import Literal, Dict
from typing import Union


class RandomNetworkRequestBase:
    random_or_predefined: Literal['random']
    number_of_nodes: int
    min_allowed_parents: int
    max_allowed_parents: int


categoricalNetworkRequestDefaults = {
    "random_or_predefined": "random",
    "number_of_nodes": 10,
    "min_allowed_parents": 1,
    "max_allowed_parents": 3,
    "categorical_or_continuous": "categorical",
    "min_allowed_mutual_information": 0.1,
    "max_allowed_mutual_information": 0.9,
    "values_per_variable": {"2": 0.7, "3": 0.25, "4": 0.05},
}


class CategoricalNetworkRequest(RandomNetworkRequestBase):
    def __init__(self, **kwargs):
        for key, default in categoricalNetworkRequestDefaults.items():
            value = kwargs.get(key, default)
            if value == "":
                value = default
            setattr(self, key, value)

    categorical_or_continuous: Literal['categorical']
    min_allowed_mutual_information: float
    max_allowed_mutual_information: float
    values_per_variable: Dict[str, float]


class ContinuousNetworkRequest:
    categorical_or_continuous: Literal['continuous']


class PredefinedNetworkRequest:
    random_or_predefined: Literal['predefined']


RandomNetworkRequest = Union[CategoricalNetworkRequest, ContinuousNetworkRequest]
GenerateNetworkRequest = Union[RandomNetworkRequest, PredefinedNetworkRequest]
