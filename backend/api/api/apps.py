# myapp/apps.py

from django.apps import AppConfig

from backend.api.cache.cache import cache
from backend.api.responseTypes.networkResponse import NetworkResponse
from backend.candidates.candidate_group import CandidateGroup
from backend.candidates.generate_candidates import generate_candidate_group
from backend.network.bayesian_network import BayesianNetwork, num_samples
from backend.network.generation.generate_network import generate_network


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        network: BayesianNetwork = generate_network()

        network_response: NetworkResponse = network.to_network_response()

        candidate_group: CandidateGroup = generate_candidate_group(network, num_samples)

        for characteristic in network.characteristics:
            network_response["characteristics"][characteristic]["priorDistribution"] \
                = candidate_group.characteristic_to_distribution(characteristic)

        cache("network", network)
        cache("network-response", network_response)
