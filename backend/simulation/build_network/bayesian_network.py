from abc import abstractmethod, ABC
from typing import List, Dict, Literal, Optional, TYPE_CHECKING

from pgmpy.models import BayesianNetwork as pgBN

from backend.api.types import ConditionRequest
from backend.api.types import NetworkResponse
from backend.simulation.build_network.characteristic import Characteristic

if TYPE_CHECKING:
    from backend.simulation.sample_applicants import Applicants

num_samples = 5000


class BayesianNetwork(ABC):
    @abstractmethod
    def __init__(
        self,
        model: Optional[pgBN] = None,
        characteristics: Optional[Dict[str, Characteristic]] = None,
        score_characteristic: str = "score",
        application_characteristics: Optional[List[str]] = None,
    ):
        if application_characteristics is None:
            application_characteristics = []
        if characteristics is None:
            characteristics = {}

        self.model: pgBN = model  # type: ignore
        self.characteristics: Dict[str, Characteristic] = characteristics
        self.score_characteristic: str = score_characteristic
        self.application_characteristics: List[str] = application_characteristics
        self.model_type: Literal["", "pgmpy"] = ""
        self.predefined = False

    def set_category_names_for_characteristic(
        self, characteristic: str, category_names: List[str]
    ):
        self.characteristics[characteristic].set_categories(category_names)

    @abstractmethod
    def to_network_response(self) -> NetworkResponse:
        pass

    @abstractmethod
    def initialise_characteristics_from_model(
        self, model: pgBN
    ) -> Dict[str, Characteristic]:
        pass

    @abstractmethod
    def sample_conditioned(self) -> Dict[str, List[float]]:
        pass

    @abstractmethod
    def sample_applicants(self, count: int = num_samples) -> "Applicants":
        pass

    @abstractmethod
    def condition_on(self, condition_request: ConditionRequest) -> None:
        pass
