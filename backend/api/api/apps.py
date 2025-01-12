# myapp/apps.py

from django.apps import AppConfig
from django.core.cache import cache

from backend.api.reponseTypes.networkResponse import NetworkResponse
from backend.candidates.candidate_group import CandidateGroup
from backend.candidates.generate_candidates import generate_candidate_group, num_samples
from backend.network.bayesian_network import BayesianNetwork
from backend.network.generate_network import generate_network


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        network: BayesianNetwork = generate_network()

        network_response: NetworkResponse = network.to_network_response()

        candidate_group: CandidateGroup = generate_candidate_group(network, num_samples)

        for characteristic in network.characteristics:
            network_response["characteristics"][characteristic]["priorDistribution"] \
                = candidate_group.characteristic_to_distribution(characteristic)

        cache.set("network", network, timeout=None)
        cache.set("network-response", network_response, timeout=None)
