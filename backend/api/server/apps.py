from django.apps import AppConfig

from backend.api.cache import cache_network_and_generate_applicants
from backend.simulation.build_network.bayesian_network import BayesianNetwork
from backend.simulation.build_network.pgmpy_network import PgmPyNetwork
from backend.simulation.build_network.predefined.random_seeded import (
    get_random_seeded_network,
    get_named_seeded_network,
)
from backend.simulation.build_network.predefined.shark_sightings import get_shark_sighting_network
from backend.simulation.build_network.predefined.sprinkler import get_sprinkler_network


class ServerConfig(AppConfig):
    name = "server"

    def ready(self):
        import sys

        if any(
            cmd in sys.argv
            for cmd in ["migrate", "makemigrations", "collectstatic", "shell"]
        ):
            return

        network: BayesianNetwork = get_sprinkler_network()
        cache_network_and_generate_applicants(network)

        sprinkler: BayesianNetwork = get_sprinkler_network()
        cache_network_and_generate_applicants(sprinkler, "sprinkler")

        shark_sightings: BayesianNetwork = get_shark_sighting_network()
        cache_network_and_generate_applicants(shark_sightings, "shark_sighting")

        random_seeded: PgmPyNetwork = get_random_seeded_network()
        cache_network_and_generate_applicants(random_seeded, "random_seeded")

        named_seeded: PgmPyNetwork = get_named_seeded_network()
        cache_network_and_generate_applicants(named_seeded, "named_seeded")
