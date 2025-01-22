from typing import List, Dict

from networkx.readwrite.json_graph import node_link_data
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork as pgBN

from backend.api.responseTypes.conditionResponse import ConditionRequest
from backend.api.responseTypes.networkResponse import NetworkResponse
from backend.network.bayesian_network import BayesianNetwork, Characteristic, num_samples
from backend.utilities.time_function import time_function


class PgmPyNetwork(BayesianNetwork):
    def __init__(self,
                 model: pgBN,
                 score_characteristic: str = "score",
                 application_characteristics: List[str] = None,
                 description: str = "",
                 observed: Dict[str, float] = None):

        super().__init__(model=None,
                         characteristics=None,
                         score_characteristic=score_characteristic,
                         application_characteristics=application_characteristics,
                         description=description)

        self.model: pgBN = model
        self.characteristics = self.initialise_characteristics_from_model(model)
        self.model_type = "pgmpy"
        self.observed = observed

    def initialise_characteristics_from_model(self, model: pgBN):
        self.characteristics = {}
        for characteristic in model.nodes:
            self.characteristics[characteristic] = Characteristic(characteristic, "categorical")
        return self.characteristics

    def to_network_response(self) -> NetworkResponse:
        return {
            "graph": node_link_data(self.model.to_directed(), link="links"),
            "scoreCharacteristic": self.score_characteristic,
            "applicationCharacteristics": self.application_characteristics,
            "characteristics": {name: characteristic.to_characteristic_response() for [name, characteristic] in
                                self.characteristics.items()},
            "description": self.description}

    def condition_on(self, condition_request: ConditionRequest) -> None:
        self.observed = condition_request

    @time_function("Sampling Posterior")
    def sample_conditioned(self):
        inference = VariableElimination(self.model)
        sampled_data = (inference.query([c for c in self.characteristics if c not in self.observed.keys()],
                                        evidence=self.observed))
        sampled_data = sampled_data.sample(num_samples)

        condition_response = {}
        for column in sampled_data:
            condition_response[column] = sampled_data[column].tolist()

        return condition_response
