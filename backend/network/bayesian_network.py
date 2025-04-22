from abc import abstractmethod, ABC
from typing import List, Dict, Union, Literal

import pymc as pm
from pgmpy.models import BayesianNetwork as pgBN

from backend.api.requestTypes.condition_request import ConditionRequest
from backend.api.responseTypes.network_response import NetworkResponse
from backend.network.characteristic import Characteristic

num_samples = 5000


class BayesianNetwork(ABC):
    @abstractmethod
    def __init__(self,
                 model: Union[pm.Model, pgBN] = None,
                 characteristics: Dict[str, Characteristic] = None,
                 score_characteristic: str = "score",
                 application_characteristics: List[str] = None):
        if application_characteristics is None:
            application_characteristics = []
        if characteristics is None:
            characteristics = {}

        self.model: Union[pm.Model, pgBN] = model
        self.characteristics: Dict[str, Characteristic] = characteristics
        self.score_characteristic: str = score_characteristic
        self.application_characteristics: List[str] = application_characteristics
        self.model_type: Union[Literal[""], Literal["pymc"], Literal["pgmpy"]] = ""
        self.predefined = False

    def set_category_names_for_characteristic(self, characteristic: str, category_names: List[str]):
        self.characteristics[characteristic].set_categories(category_names)

    @abstractmethod
    def to_network_response(self) -> NetworkResponse:
        pass

    @abstractmethod
    def initialise_characteristics_from_model(self, model: Union[pm.Model, pgBN]):
        pass

    @abstractmethod
    def sample_conditioned(self) -> Dict[str, List[float]]:
        pass

    @abstractmethod
    def condition_on(self, condition_request: ConditionRequest) -> None:
        pass
