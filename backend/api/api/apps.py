from django.apps import AppConfig

from backend.api.api.cache_network import cache_network_and_generate_candidates
from backend.network.bayesian_network import BayesianNetwork
from backend.network.example_networks.sprinkler import get_sprinkler_network


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        network: BayesianNetwork = get_sprinkler_network()
        cache_network_and_generate_candidates(network)
