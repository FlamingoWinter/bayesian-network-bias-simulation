# myapp/apps.py

import pymc as pm
from django.apps import AppConfig
from django.core.cache import cache
from django.http import JsonResponse
from networkx.readwrite.json_graph import node_link_data

from backend.api.reponseTypes.distributionResponse import DistributionResponse
from backend.api.reponseTypes.networkResponse import NetworkResponse
from backend.candidates.candidate_group import CandidateGroup
from backend.candidates.generate_candidates import generate_candidate_group
from backend.network.bayesian_network import BayesianNetwork
from backend.network.generate_network import generate_network


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        network: BayesianNetwork = generate_network()

        network_response: NetworkResponse = {
            "graph": node_link_data(pm.model_to_networkx(network.model), link="links"),
            "scoreCharacteristic": network.score_characteristic,
            "applicationCharacteristics": network.application_characteristics,
            "descriptionsByCharacteristic": network.descriptions_by_characteristic,
            "description": network.description}

        cache.set("network",
                  JsonResponse(network_response, safe=False),
                  timeout=None)

        candidate_group: CandidateGroup = generate_candidate_group(network, 10_000)
        for node in network.model.named_vars:
            if node in network.categories_by_categorical_variable.keys():
                categories_for_categorical_distributions = network.categories_by_categorical_variable[node]
                distribution_type = "categorical"
            else:
                categories_for_categorical_distributions = None
                if node in [var.name for var in network.model.discrete_value_vars]:
                    distribution_type = "discrete"
                else:
                    distribution_type = "continuous"

            distribution_response: DistributionResponse = {
                "distribution": candidate_group.characteristics[node].to_list(),
                "distributionType": distribution_type,
                "categoriesForCategoricalDistributions": categories_for_categorical_distributions}

            cache.set(f"prior-distribution-{node}",
                      JsonResponse(distribution_response, safe=False),
                      timeout=None)
