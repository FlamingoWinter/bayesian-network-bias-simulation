# myapp/apps.py

from django.apps import AppConfig

from backend.api.api.cache_network import cache_network
from backend.network.bayesian_network import BayesianNetwork
from backend.network.generation.generate_network import generate_network


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        network: BayesianNetwork = generate_network()

        cache_network(network)
