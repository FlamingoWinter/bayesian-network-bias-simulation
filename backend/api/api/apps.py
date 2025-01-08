# myapp/apps.py
import pymc as pm
from django.apps import AppConfig
from django.core.cache import cache
from django.http import JsonResponse
from networkx.readwrite.json_graph import node_link_data

from backend.candidates.candidate_generation import generate_candidate_group
from backend.candidates.candidate_group import CandidateGroup
from backend.network.bayesian_network import BayesianNetwork
from backend.network.network_generation import generate_network


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        network: BayesianNetwork = generate_network()
        cache.set("network",
                  JsonResponse(node_link_data(pm.model_to_networkx(network.model), link="links"), safe=False),
                  timeout=None)

        candidate_group: CandidateGroup = generate_candidate_group(network, 1000)
        for node in network.model.named_vars:
            if node in network.categories_by_categorical_variable.keys():
                categories_for_categorical_distributions = network.categories_by_categorical_variable[node]
                is_categorical_variable = True
            else:
                categories_for_categorical_distributions = None
                is_categorical_variable = False

            cache.set(f"prior-distribution-{node}",
                      JsonResponse(
                          {"distribution": candidate_group.characteristics[node].to_list(),
                           "isCategoricalVariable": True,
                           "categoriesForCategoricalDistributions": categories_for_categorical_distributions}
                          , safe=False),
                      timeout=None)
