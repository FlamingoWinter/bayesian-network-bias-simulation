from typing import List, Dict

import numpy as np
from networkx.readwrite.json_graph import node_link_data
from pgmpy.models import BayesianNetwork as pgBN
from pgmpy.sampling import BayesianModelSampling
from pgmpy.sampling.Sampling import State

from backend.api.responseTypes.networkResponse import NetworkResponse
from backend.network.bayesian_network import BayesianNetwork, Characteristic, num_samples
from backend.utilities.time_function import time_function


class PgmPyNetwork(BayesianNetwork):
    def __init__(self,
                 model: pgBN,
                 score_characteristic: str = "score",
                 application_characteristics: List[str] = None,
                 description: str = "",
                 observed: Dict[str, np.array] = None):

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

    @time_function("Sampling Posterior")
    def sample_conditioned(self):
        sampler = BayesianModelSampling(self.model)
        evidence = [State(var=key, state=value) for key, value in self.observed.items()]

        sampled_data = sampler.rejection_sample(evidence=evidence, size=num_samples)

        condition_response = {}
        for column in sampled_data.columns:
            condition_response[column] = sampled_data[column].tolist()

        return condition_response
