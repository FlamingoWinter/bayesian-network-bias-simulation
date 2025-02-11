from typing import Literal, List
from typing import Union


class SimulateRequestBase:
    candidates_to_generate: int
    train_proportion: float
    recruiters: List[str]
    protected_characteristic: str


categoricalNetworkRequestDefaults = {
    "categorical_or_continuous": "categorical",
    "candidates_to_generate": 1_000_000,
    "train_proportion": 0.9,
    "recruiters": ["Random Forest Recruiter"],
    "protected_characteristic": ""
}


class CategoricalSimulateRequest(SimulateRequestBase):
    def __init__(self, **kwargs):
        for key, default in categoricalNetworkRequestDefaults.items():
            value = kwargs.get(key, default)
            if value == "":
                value = default
            setattr(self, key, value)

    categorical_or_continuous: Literal['categorical']


class ContinuousSimulateRequest(SimulateRequestBase):
    categorical_or_continuous: Literal['continuous']
    score_threshold: float


SimulateRequest = Union[CategoricalSimulateRequest, ContinuousSimulateRequest]


def new_simulate_request(**kwargs) -> SimulateRequest:
    if kwargs.get("categorical_or_continuous") == "categorical":
        return CategoricalSimulateRequest(**kwargs)

    if kwargs.get("categorical_or_continuous") == "continuous":
        if "score_threshold" not in kwargs:
            raise ValueError("ContinuousSimulateRequest requires 'score_threshold'")
        return ContinuousSimulateRequest(**kwargs)
