from dataclasses import field, dataclass
from typing import Literal, Dict, Tuple, Union

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
    mutual_information_range: Tuple[float, float] = (0.1, 0.9)
    values_per_variable: Dict[str, float] = field(default_factory=lambda: {"2": 0.7, "3": 0.25, "4": 0.05})


class PredefinedNetworkRequest(NetworkRequestBase):
    random_or_predefined: Literal['predefined']
    predefined_model: str


GenerateNetworkRequest = Union[CategoricalNetworkRequest, PredefinedNetworkRequest]


def new_random_network_request(**kwargs) -> CategoricalNetworkRequest:
    kwargs = replace_blanks_with_defaults(kwargs, CategoricalNetworkRequest)
    kwargs.pop("predefined_model", None)
    return CategoricalNetworkRequest(**kwargs)
