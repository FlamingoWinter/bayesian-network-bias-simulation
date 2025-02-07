from typing import List, Dict

import networkx as nx
from networkx.readwrite.json_graph import node_link_data
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork as pgBN

from backend.api.responseTypes.conditionResponse import ConditionRequest
from backend.api.responseTypes.networkResponse import NetworkResponse
from backend.network.bayesian_network import BayesianNetwork, Characteristic, num_samples
from backend.utilities.time_function import time_function


class CharacteristicName:
    def __init__(self, name: str, values: List[str] = None, hml=False):
        self.name = name
        self.values = values
        self.hml = hml

    def set_number_values(self, num_values: int) -> 'CharacteristicName':
        if self.hml:
            self.values = ["V. High", "High", "Medium", "Low", "V. Low"]
            if num_values == 2:
                self.values = ["High", "Low"]
            if num_values == 3:
                self.values = ["High", "Medium", "Low"]
            if num_values == 4:
                self.values = ["Very High", "High", "Low", "Very Low"]
        if num_values is not None:
            self.values = self.values[:num_values]

        return self


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

        self.name_mapping: Dict[str, str] = None
        self.inv_name_mapping = None
        self.model: pgBN = model
        self.characteristics: Dict[str, Characteristic] = self.initialise_characteristics_from_model(model)
        self.model_type = "pgmpy"
        self.observed = observed

    def rename_nodes(self, old_to_new: Dict[str, CharacteristicName]):
        self.name_mapping = {old_node: new_characteristic.name for [old_node, new_characteristic] in old_to_new.items()}
        self.inv_name_mapping = {v: k for k, v in self.name_mapping.items()}
        new_characteristics = {}
        for _, characteristic in self.characteristics.items():
            old_name = characteristic.name
            new_characteristic = old_to_new[old_name]
            characteristic.set_categories(new_characteristic.values)
            characteristic.name = new_characteristic.name
            new_characteristics[characteristic.name] = characteristic
        self.characteristics = new_characteristics

    def initialise_characteristics_from_model(self, model: pgBN):
        self.characteristics = {}
        for characteristic in model.nodes:
            self.characteristics[characteristic] = Characteristic(characteristic, "categorical")
        return self.characteristics

    def to_network_response(self) -> NetworkResponse:
        directed_graph = self.model.to_directed()
        score_characteristic = self.score_characteristic
        application_characteristics = self.application_characteristics

        if self.name_mapping is not None:
            directed_graph = nx.relabel_nodes(directed_graph, self.name_mapping)
            score_characteristic = self.name_mapping[score_characteristic]
            application_characteristics = [self.name_mapping[c] for c in application_characteristics]

        return {
            "graph": node_link_data(directed_graph, link="links"),
            "scoreCharacteristic": score_characteristic,
            "applicationCharacteristics": application_characteristics,
            "characteristics": {name: characteristic.to_characteristic_response() for [name, characteristic] in
                                self.characteristics.items()},
            "description": self.description,
            "predefined": self.predefined}

    def condition_on(self, condition_request: ConditionRequest) -> None:
        if self.name_mapping is None:
            self.observed = condition_request
        else:
            self.observed = {self.inv_name_mapping[new_characteristic]: value for new_characteristic, value in
                             condition_request.items()}

    @time_function("Sampling Posterior")
    def sample_conditioned(self):
        inference = VariableElimination(self.model)
        model_formatted_characteristics = self.characteristics.keys()
        if self.name_mapping is not None:
            model_formatted_characteristics = [self.inv_name_mapping[c] for c in model_formatted_characteristics]

        sampled_data = (inference.query([c for c in model_formatted_characteristics if c not in self.observed.keys()],
                                        evidence=self.observed))
        sampled_data = sampled_data.sample(num_samples)

        condition_response = {}
        for column in sampled_data:
            if self.name_mapping is None:
                condition_response[column] = sampled_data[column].tolist()
            else:
                condition_response[self.name_mapping[column]] = sampled_data[column].tolist()

        return condition_response
