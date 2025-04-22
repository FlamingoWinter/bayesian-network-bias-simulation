from collections import Counter
from typing import List, Dict, Union

import networkx as nx
from networkx.readwrite.json_graph import node_link_data
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork as pgBN

from backend.api.requestTypes.condition_request import ConditionRequest
from backend.api.responseTypes.network_response import NetworkResponse
from backend.applicants.applicants import Applicants
from backend.applicants.sample_applicants import sample_applicants
from backend.network.bayesian_network import BayesianNetwork, Characteristic, num_samples
from backend.network.naming_characteristics.name_characteristics import CharacteristicName
from backend.utilities.time_function import time_function


class PgmPyNetwork(BayesianNetwork):
    def __init__(self,
                 model: pgBN,
                 score_characteristic: str = "score",
                 application_characteristics: List[str] = None,
                 observed: Dict[str, float] = None):

        super().__init__(model=None,
                         characteristics=None,
                         score_characteristic=score_characteristic,
                         application_characteristics=application_characteristics)

        self.renaming: Union[Dict[str, str], None] = None
        self.inverse_renaming = None
        self.model: pgBN = model
        self.characteristics: Dict[str, Characteristic] = self.initialise_characteristics_from_model(model)
        self.model_type = "pgmpy"
        self.observed = observed

    def rename_nodes(self, old_to_new: Dict[str, CharacteristicName]):
        self.renaming = {old_node: new_characteristic.name for [old_node, new_characteristic] in old_to_new.items()}
        self.inverse_renaming = {v: k for k, v in self.renaming.items()}
        new_characteristics = {}
        for _, characteristic in self.characteristics.items():
            old_name = characteristic.name
            new_characteristic = old_to_new[old_name]
            characteristic.set_categories(new_characteristic.values)
            characteristic.name = new_characteristic.name
            new_characteristics[characteristic.name] = characteristic
        self.characteristics = new_characteristics
        self.application_characteristics = [self.renaming[old_ac] for old_ac in self.application_characteristics]
        self.score_characteristic = self.renaming[self.score_characteristic]

    def initialise_characteristics_from_model(self, model: pgBN):
        self.characteristics = {}
        for characteristic in model.nodes:
            self.characteristics[characteristic] = Characteristic(characteristic, "categorical")
        return self.characteristics

    def to_network_response(self) -> NetworkResponse:
        directed_graph = self.model.to_directed()
        score_characteristic = self.score_characteristic
        application_characteristics = self.application_characteristics

        if self.renaming is not None:
            directed_graph = nx.relabel_nodes(directed_graph, self.renaming)

        applicants: Applicants = sample_applicants(self, num_samples)

        characteristic_responses = {}
        for characteristic_name, characteristic in self.characteristics.items():
            distribution = applicants.characteristic_name_to_distribution(characteristic_name)
            value_counts = Counter(distribution)
            expected_values = range(max(value_counts.keys(), default=0) + 1)
            prior_distribution = [value_counts.get(x, 0) / len(distribution) for x in expected_values]
            characteristic_responses[characteristic.name] = characteristic.to_characteristic_response(
                prior_distribution)

        return {
            "graph": node_link_data(directed_graph, link="links"),
            "scoreCharacteristic": score_characteristic,
            "applicationCharacteristics": application_characteristics,
            "characteristics": characteristic_responses,
            "predefined": self.predefined}

    def condition_on(self, condition_request: ConditionRequest) -> None:
        if self.renaming is None:
            self.observed = condition_request
        else:
            self.observed = {self.inverse_renaming[new_characteristic]: value for new_characteristic, value in
                             condition_request.items()}

    @time_function("Sampling Posterior")
    def sample_conditioned(self):
        if len(self.model.nodes) > 22:
            raise "Error! Too many nodes for variable elimination"
        inference = VariableElimination(self.model)

        model_formatted_characteristics = self.characteristics.keys()
        if self.renaming is not None:
            model_formatted_characteristics = [self.inverse_renaming[c] for c in model_formatted_characteristics]

        sampled_data = (inference.query([c for c in model_formatted_characteristics if c not in self.observed.keys()],
                                        evidence=self.observed, show_progress=True))
        sampled_data = sampled_data.sample(num_samples)

        condition_response = {}
        for column in sampled_data:
            total_count = len(sampled_data[column])
            value_counts = Counter(sampled_data[column])

            expected_values = range(max(value_counts.keys(), default=0) + 1)
            proportions = [value_counts.get(x, 0) / total_count for x in expected_values]
            if self.renaming is None:
                condition_response[column] = proportions
            else:
                condition_response[self.renaming[column]] = proportions

        return condition_response
