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
                nums_to_categories = [network.categories_by_categorical_variable[node][characteristic_num]
                                      for characteristic_num in candidate_group.characteristics[node].to_list()]

                cache.set(f"distribution-{node}",
                          JsonResponse(nums_to_categories, safe=False),
                          timeout=None)
            else:
                cache.set(f"distribution-{node}",
                          JsonResponse(candidate_group.characteristics[node].to_list(), safe=False),
                          timeout=None)
