import random
from collections import Counter
from typing import List, Dict, Union

import networkx as nx
from networkx.readwrite.json_graph import node_link_data
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork as pgBN
from pgmpy.sampling import BayesianModelSampling

from backend.api.request_types.condition_request import ConditionRequest
from backend.api.response_types.network_response import NetworkResponse
from backend.applicants.applicants import Applicants
from backend.network.bayesian_network import BayesianNetwork, Characteristic, num_samples
from backend.network.naming_characteristics.name_characteristics import CharacteristicName, affected_characteristics, \
    hide_protected_characteristics, protected_characteristics, affector_characteristics, intermediary_characteristics, \
    score_characteristic
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

        applicants: Applicants = self.sample_applicants(num_samples)

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

    def sample_applicants(self, count=num_samples):
        sampler = BayesianModelSampling(self.model)
        sampled_data = sampler.forward_sample(size=count)

        if self.renaming is None:
            applicants = Applicants(self, sampled_data)
        else:
            applicants = Applicants(self, sampled_data.rename(columns=self.renaming))

        return applicants

    def name_characteristics(self, seed=None) -> 'PgmPyNetwork':
        if seed:
            random.seed(seed)

        old_to_new: Dict[str, CharacteristicName] = {}

        graph = self.model.to_directed()

        # 1) Characteristics affected (directly or indirectly) by job competency should be affected_characteristics.
        score_descendants = nx.descendants(graph, self.score_characteristic)
        affected_characteristic_choices = random.sample(affected_characteristics, len(score_descendants))
        for score_descendant, affected_characteristic in zip(score_descendants,
                                                             affected_characteristic_choices):
            old_to_new[score_descendant] = affected_characteristic

        # 2) Characteristics affected by nothing should be protected.
        nodes_without_ancestors = [node for node, deg in graph.in_degree() if deg == 0]
        if hide_protected_characteristics:
            protected_characteristic_choices = [
                CharacteristicName(f"Protected Characteristic {i + 1}", ["1", "2", "3", "4", "5"]) for i in
                range(len(nodes_without_ancestors))]
        else:
            protected_characteristic_choices = random.sample(protected_characteristics, len(nodes_without_ancestors))

        for node_without_ancestor, protected_characteristic in zip(nodes_without_ancestors,
                                                                   protected_characteristic_choices):
            old_to_new[node_without_ancestor] = protected_characteristic

        # 3) Direct predecessors of job competency should be affector characteristics

        direct_predecessors = list(graph.predecessors(self.score_characteristic))
        affector_characteristic_choices = random.sample(affector_characteristics, len(direct_predecessors))
        for direct_predecessor, affector_characteristic in zip(direct_predecessors,
                                                               affector_characteristic_choices):
            old_to_new[direct_predecessor] = affector_characteristic

        # 4) Direct Children of Protected Characteristics should be Intermediary
        # Other Characteristics should be Intermediary
        direct_children = list(set([child for p in nodes_without_ancestors for child in graph.successors(p)]))
        unnamed_nodes = [node for node in graph.nodes if node != self.score_characteristic
                         and node not in score_descendants
                         and node not in nodes_without_ancestors
                         and node not in direct_predecessors
                         and node not in direct_children]

        nodes_to_be_intermediary = list(set(direct_children + unnamed_nodes))

        intermediary_characteristic_choices = random.sample(intermediary_characteristics, len(nodes_to_be_intermediary))
        for node_to_be_intermediary, intermediary_characteristic in zip(nodes_to_be_intermediary,
                                                                        intermediary_characteristic_choices):
            old_to_new[node_to_be_intermediary] = intermediary_characteristic

        # 5) Score Characteristic should be job competency.
        old_to_new[self.score_characteristic] = score_characteristic

        # -----------------------------------------------------------------------------------------------------

        for old_name, characteristic_name in old_to_new.items():
            characteristic_name.set_number_values(len(self.characteristics[old_name].category_names))

        self.rename_nodes(old_to_new)
        return self
