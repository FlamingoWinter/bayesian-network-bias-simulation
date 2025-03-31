from dataclasses import field, dataclass
from typing import Literal, Dict, Tuple
from typing import Union

from backend.utilities.replace_blanks_with_defaults import replace_blanks_with_defaults


class NetworkRequestBase:
    random_or_predefined: Literal['random', 'predefined']


class RandomNetworkRequestBase(NetworkRequestBase):
    random_or_predefined: Literal['random']
    number_of_nodes: int
    parents_range: Tuple[int, int]


@dataclass
class CategoricalNetworkRequest(RandomNetworkRequestBase):
    random_or_predefined: Literal['random'] = "random"
    number_of_nodes: int = 12
    parents_range: Tuple[int, int] = (1, 3)
    categorical_or_continuous: Literal['categorical'] = "categorical"
    mutual_information_range: Tuple[float, float] = (0.1, 0.9)
    values_per_variable: Dict[str, float] = field(default_factory=lambda: {"2": 0.7, "3": 0.25, "4": 0.05})


@dataclass
class ContinuousNetworkRequest(RandomNetworkRequestBase):
    categorical_or_continuous: Literal['continuous'] = "continuous"


class PredefinedNetworkRequest(NetworkRequestBase):
    random_or_predefined: Literal['predefined']


RandomNetworkRequest = Union[CategoricalNetworkRequest, ContinuousNetworkRequest]
GenerateNetworkRequest = Union[RandomNetworkRequest, PredefinedNetworkRequest]


def new_generate_network_request(**kwargs) -> GenerateNetworkRequest:
    if kwargs.get("random_or_predefined") == "predefined":
        return PredefinedNetworkRequest()

    if kwargs.get("categorical_or_continuous") == "categorical":
        kwargs = replace_blanks_with_defaults(kwargs, CategoricalNetworkRequest)
        return CategoricalNetworkRequest(**kwargs)

    if kwargs.get("categorical_or_continuous") == "continuous":
        return ContinuousNetworkRequest()
