from typing import List, Dict, cast

import pymc as pm
from networkx.readwrite.json_graph import node_link_data

from backend.api.reponseTypes.conditionResponse import ConditionResponse
from backend.api.reponseTypes.networkResponse import CharacteristicResponse, NetworkResponse, DistributionType
from backend.type_extensions.prior_trace import PosteriorTrace
from backend.utilities.time_function import time_function

num_samples = 10_000


class BayesianNetwork:
    def __init__(self,
                 pm_model: pm.Model,
                 score_characteristic: str = "score",
                 application_characteristics: List[str] = None,
                 description: str = ""):

        if application_characteristics is None:
            application_characteristics = []

        self.model = pm_model
        self.characteristics: Dict[str, Characteristic] = self.initialise_characteristics_from_model(pm_model)
        self.score_characteristic: str = score_characteristic
        self.application_characteristics: List[str] = application_characteristics
        self.description: str = description

    def set_description_for_characteristic(self, characteristic: str, description: str):
        self.characteristics[characteristic].description = description

    def set_category_names_for_characteristic(self, characteristic: str, category_names: List[str]):

        self.characteristics[characteristic].set_categories(category_names)

    def set_description(self, description: str):
        self.description = description

    def to_network_response(self) -> NetworkResponse:
        return {
            "graph": node_link_data(pm.model_to_networkx(self.model), link="links"),
            "scoreCharacteristic": self.score_characteristic,
            "applicationCharacteristics": self.application_characteristics,
            "characteristics": {name: characteristic.to_characteristic_response() for [name, characteristic] in
                                self.characteristics.items()},
            "description": self.description}

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
            'priorDistribution': None,
            'posteriorDistribution': None
        }
