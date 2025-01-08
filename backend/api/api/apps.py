# myapp/apps.py

import pymc as pm
from django.apps import AppConfig
from django.core.cache import cache
from django.http import JsonResponse
from networkx.readwrite.json_graph import node_link_data

from backend.api.reponseTypes.distributionResponse import DistributionResponse
from backend.api.reponseTypes.networkResponse import NetworkResponse
from backend.candidates.candidate_generation import generate_candidate_group
from backend.candidates.candidate_group import CandidateGroup
from backend.network.bayesian_network import BayesianNetwork
from backend.network.network_generation import generate_network


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        network: BayesianNetwork = generate_network()

        network_response: NetworkResponse = {
            "network": node_link_data(pm.model_to_networkx(network.model), link="links"),
            "scoreCharacteristic": network.score_characteristic,
            "applicationCharacteristics": network.application_characteristics}

        cache.set("network",
                  JsonResponse(network_response, safe=False),
                  timeout=None)

        candidate_group: CandidateGroup = generate_candidate_group(network, 1000)
        for node in network.model.named_vars:
            if node in network.categories_by_categorical_variable.keys():
                categories_for_categorical_distributions = network.categories_by_categorical_variable[node]
                is_categorical_variable = True
            else:
                categories_for_categorical_distributions = None
                is_categorical_variable = False

            distribution_response: DistributionResponse = {
                "distribution": candidate_group.characteristics[node].to_list(),
                "isCategoricalVariable": True,
                "categoriesForCategoricalDistributions": categories_for_categorical_distributions}

            cache.set(f"prior-distribution-{node}",
                      JsonResponse(distribution_response, safe=False),
                      timeout=None)
