import json
from typing import Any

from scipy.stats import rv_discrete

from backend.api.api.cache_network import cache_network_and_generate_candidates
from backend.api.api.consumers.generic_consumer import GenericConsumer
from backend.api.requestTypes.generate_network_request import RandomNetworkRequest, new_categorical_network_request
from backend.network.generation.generate_categorical_network import generate_random_categorical_network
from backend.network.pgmpy_network import PgmPyNetwork


class GenerateRandomNetworkConsumer(GenericConsumer):
    session_key: str

    async def receive(self,
                      text_data: Any = None,
                      bytes_data: Any = None) -> None:
        request: RandomNetworkRequest = new_categorical_network_request(**json.loads(text_data))

        category_number_dist = rv_discrete(
            values=([int(x) for x in request.values_per_variable.keys()],
                    list(request.values_per_variable.values())))

        network: PgmPyNetwork = generate_random_categorical_network(int(request.number_of_nodes),
                                                                    tuple(map(int, request.parents_range)),
                                                                    tuple(map(float, request.mutual_information_range)),
                                                                    category_number_dist)

        await self.send_and_flush(f"Network Generation Completed")

        cache_network_and_generate_candidates(network, self.session_key)

        await self.send_and_flush(f"Candidate Generation Completed")

        await self.close(code=1000)
