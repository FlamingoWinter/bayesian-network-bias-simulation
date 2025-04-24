import json
from typing import Any

from scipy.stats import rv_discrete

from backend.api.api.consumers.generic_consumer import GenericConsumer
from backend.api.cache import cache_network_and_generate_applicants
from backend.api.request_types.generate_network_request import RandomNetworkRequest, new_random_network_request
from backend.network.generation.generate_categorical_network import generate_random_categorical_network
from backend.network.pgmpy_network import PgmPyNetwork
from backend.network.predefined.random_seeded import get_random_seeded_network, get_named_seeded_network
from backend.network.predefined.shark_sightings import get_shark_sighting_network
from backend.network.predefined.sprinkler import get_sprinkler_network


class GenerateRandomNetworkConsumer(GenericConsumer):
    async def receive(self,
                      text_data: Any = None,
                      bytes_data: Any = None) -> None:
        raw_request = json.loads(text_data)

        if raw_request["random_or_predefined"] == "predefined":
            predefined_model = raw_request["predefined_model"]
            if predefined_model == "sprinkler":
                network = get_sprinkler_network()
            elif predefined_model == "shark_sighting":
                network = get_shark_sighting_network()
            elif predefined_model == "random_seeded":
                network = get_random_seeded_network()
            elif predefined_model == "named_seeded":
                network = get_named_seeded_network()
            else:
                await self.send_and_flush("Predefined model name was incorrect", error=True)
                await self.close(code=1000)
                return
        else:
            request: RandomNetworkRequest = new_random_network_request(**raw_request)

            category_number_distribution = rv_discrete(
                values=([int(x) for x in request.values_per_variable.keys()],
                        list(request.values_per_variable.values())))

            network: PgmPyNetwork = generate_random_categorical_network(int(request.number_of_nodes),
                                                                        (int(request.parents_range[0]),
                                                                         int(request.parents_range[1])),
                                                                        (int(request.mutual_information_range[0]),
                                                                         request.mutual_information_range[1]),
                                                                        category_number_distribution)

        await self.send_and_flush(f"Network Generation Completed")
        cache_network_and_generate_applicants(network, self.session_key)
        await self.send_and_flush(f"Candidate Generation Completed")
        await self.close(code=1000)
