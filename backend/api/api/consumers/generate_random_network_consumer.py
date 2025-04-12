import json
from typing import Any

from scipy.stats import rv_discrete

from backend.api.api.cache_network import cache_network_and_generate_candidates
from backend.api.api.consumers.generic_consumer import GenericConsumer
from backend.api.requestTypes.generate_network_request import RandomNetworkRequest, new_categorical_network_request
from backend.network.bayesian_network import BayesianNetwork
from backend.network.example_networks.shark_sightings import get_shark_sighting_network
from backend.network.example_networks.sprinkler import get_sprinkler_network
from backend.network.generation.generate_categorical_network import generate_random_categorical_network
from backend.network.naming_characteristics.name_characteristics import name_characteristics
from backend.network.pgmpy_network import PgmPyNetwork, CharacteristicName


class GenerateRandomNetworkConsumer(GenericConsumer):
    session_key: str

    async def receive(self,
                      text_data: Any = None,
                      bytes_data: Any = None) -> None:
        req = json.loads(text_data)
        print(req)

        if req["random_or_predefined"] == "predefined":
            network = get_sprinkler_network()
            if req["predefined_model"] == "sprinkler":
                network: BayesianNetwork = get_sprinkler_network()
            if req["predefined_model"] == "shark_sighting":
                network: BayesianNetwork = get_shark_sighting_network()
            if req["predefined_model"] == "random_seeded":
                network: PgmPyNetwork = generate_random_categorical_network(
                    20,
                    (2, 3),
                    (0.6, 0.9),
                    seed=967
                )
                network.rename_nodes({c.name: CharacteristicName(
                    "Protected Characteristic" if c.name == "0" else
                    "Competence" if c.name == "17" else
                    "19" if c.name == "19" else c.name, c.category_names)
                    for c in network.characteristics.values()})

            if req["predefined_model"] == "named_seeded":
                network: PgmPyNetwork = generate_random_categorical_network(
                    20,
                    (2, 3),
                    (0.6, 0.9),
                    seed=967
                )
                network.score_characteristic = "19"
                network = name_characteristics(network, seed=957)

            await self.send_and_flush(f"Network Generation Completed")
            cache_network_and_generate_candidates(network, self.session_key)
            await self.send_and_flush(f"Candidate Generation Completed")
            await self.close(code=1000)

        else:
            request: RandomNetworkRequest = new_categorical_network_request(**req)

            category_number_dist = rv_discrete(
                values=([int(x) for x in request.values_per_variable.keys()],
                        list(request.values_per_variable.values())))

            network: PgmPyNetwork = generate_random_categorical_network(int(request.number_of_nodes),
                                                                        tuple(map(int, request.parents_range)),
                                                                        tuple(map(float,
                                                                                  request.mutual_information_range)),
                                                                        category_number_dist)

            await self.send_and_flush(f"Network Generation Completed")

            cache_network_and_generate_candidates(network, self.session_key)

            await self.send_and_flush(f"Candidate Generation Completed")

            await self.close(code=1000)
