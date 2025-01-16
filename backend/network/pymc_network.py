from typing import List, cast

import pymc as pm
from networkx.readwrite.json_graph import node_link_data

from backend.api.responseTypes.conditionResponse import ConditionResponse
from backend.api.responseTypes.networkResponse import DistributionType, NetworkResponse
from backend.network.bayesian_network import BayesianNetwork, Characteristic, num_samples
from backend.type_extensions.prior_trace import PosteriorTrace
from backend.utilities.time_function import time_function


class PyMcNetwork(BayesianNetwork):
    def __init__(self,
                 model: pm.Model,
                 score_characteristic: str = "score",
                 application_characteristics: List[str] = None,
                 description: str = ""):

        super().__init__(model=None,
                         characteristics=None,
                         score_characteristic=score_characteristic,
                         application_characteristics=application_characteristics,
                         description=description)

        self.model: pm.Model = model
        self.characteristics = self.initialise_characteristics_from_model(model)
        self.model_type = "pymc"

    def initialise_characteristics_from_model(self, model: pm.Model):
        self.characteristics = {}
        for characteristic in model.named_vars:
            distribution_type: DistributionType
            if characteristic in [var.name for var in model.discrete_value_vars]:
                distribution_type = "discrete"
            else:
                distribution_type = "continuous"

            self.characteristics[characteristic] = Characteristic(characteristic, distribution_type)
        return self.characteristics

    def to_network_response(self) -> NetworkResponse:
        pass
        return {
            "graph": node_link_data(pm.model_to_networkx(self.model), link="links"),
            "scoreCharacteristic": self.score_characteristic,
            "applicationCharacteristics": self.application_characteristics,
            "characteristics": {name: characteristic.to_characteristic_response() for [name, characteristic] in
                                self.characteristics.items()},
            "description": self.description}

    @time_function("Sampling Posterior")
    def sample_conditioned(self):
        model = self.model

        with model:
            posterior: PosteriorTrace = cast(PosteriorTrace,
                                             pm.sample(num_samples // 4, return_inferencedata=True, cores=1, chains=4))

        condition_response: ConditionResponse = {}
        for characteristic in model.named_vars:
            if characteristic in [var for var in posterior.posterior]:
                condition_response[characteristic] = [item for sublist in
                                                      posterior.posterior[characteristic].values.tolist() for item in
                                                      sublist]

        return condition_response
