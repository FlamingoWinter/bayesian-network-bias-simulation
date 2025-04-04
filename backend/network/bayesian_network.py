from abc import abstractmethod, ABC
from typing import List, Dict, Union, Literal

import pymc as pm
from pgmpy.models import BayesianNetwork as pgBN

from backend.api.responseTypes.conditionResponse import ConditionRequest
from backend.api.responseTypes.networkResponse import CharacteristicResponse, NetworkResponse, DistributionType

num_samples = 5000


class Characteristic:
    def __init__(self, name: str, distribution_type: DistributionType):
        self.name: str = name
        self.description: str = ""
        self.type: DistributionType = distribution_type
        self.category_names: List[str] = []

    def set_description(self, description):
        self.description = description

    def set_categories(self, category_names):
        self.type = "categorical"
        self.category_names = category_names

    def to_characteristic_response(self) -> CharacteristicResponse:
        return {
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'categoryNames': self.category_names,
            'priorDistribution': None
        }


class BayesianNetwork(ABC):
    @abstractmethod
    def __init__(self,
                 model: Union[pm.Model, pgBN] = None,
                 characteristics: Dict[str, Characteristic] = None,
                 score_characteristic: str = "score",
                 application_characteristics: List[str] = None,
                 description: str = ""):
        if application_characteristics is None:
            application_characteristics = []
        if characteristics is None:
            characteristics = {}

        self.model: Union[pm.Model, pgBN] = model
        self.characteristics: Dict[str, Characteristic] = characteristics
        self.score_characteristic: str = score_characteristic
        self.application_characteristics: List[str] = application_characteristics
        self.description: str = description
        self.model_type: Union[Literal[""], Literal["pymc"], Literal["pgmpy"]] = ""
        self.predefined = False

    def set_description_for_characteristic(self, characteristic: str, description: str):
        self.characteristics[characteristic].description = description

    def set_category_names_for_characteristic(self, characteristic: str, category_names: List[str]):
        self.characteristics[characteristic].set_categories(category_names)

    def set_description(self, description: str):
        self.description = description

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
