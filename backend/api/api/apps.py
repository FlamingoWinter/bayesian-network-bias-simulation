from django.apps import AppConfig

from backend.api.api.cache_network import cache_network_and_generate_candidates
from backend.network.bayesian_network import BayesianNetwork
from backend.network.example_networks.shark_sightings import get_shark_sighting_network
from backend.network.example_networks.sprinkler import get_sprinkler_network
from backend.network.generation.generate_categorical_network import generate_random_categorical_network
from backend.network.naming_characteristics.name_characteristics import name_characteristics
from backend.network.pgmpy_network import PgmPyNetwork, CharacteristicName


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        network: BayesianNetwork = get_sprinkler_network()
        cache_network_and_generate_candidates(network)

        sprinkler: BayesianNetwork = get_sprinkler_network()
        cache_network_and_generate_candidates(sprinkler, "sprinkler")

        shark_sightings: BayesianNetwork = get_shark_sighting_network()
        cache_network_and_generate_candidates(shark_sightings, "shark_sighting")

        random_seeded: PgmPyNetwork = generate_random_categorical_network(
            20,
            (2, 3),
            (0.6, 0.9),
            seed=967
        )
        random_seeded.rename_nodes({c.name: CharacteristicName(
            "Protected Characteristic" if c.name == "0" else
            "Competence" if c.name == "17" else
            "19" if c.name == "19" else c.name, c.category_names)
            for c in random_seeded.characteristics.values()})
        cache_network_and_generate_candidates(random_seeded, "random_seeded")

        named_seeded: PgmPyNetwork = generate_random_categorical_network(
            20,
            (2, 3),
            (0.6, 0.9),
            seed=967
        )
        named_seeded.score_characteristic = "19"
        named_seeded = name_characteristics(named_seeded, seed=957)
        cache_network_and_generate_candidates(named_seeded, "named_seeded")
