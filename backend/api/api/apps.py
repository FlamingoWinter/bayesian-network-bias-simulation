# myapp/apps.py

from django.apps import AppConfig
from django.core.cache import cache
from django.http import JsonResponse

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

        network_response: NetworkResponse = network.to_network_response()
        network_response_json = JsonResponse(network_response, safe=False)

        cache.set("network", network_response_json, timeout=None)

        candidate_group: CandidateGroup = generate_candidate_group(network, 10_000)

        for node in network.model.named_vars:
            distribution_response: DistributionResponse = candidate_group.characteristic_to_distribution_response(node)
            distribution_response_json = JsonResponse(distribution_response, safe=False)

            cache.set(f"prior-distribution-{node}", distribution_response_json, timeout=None)
