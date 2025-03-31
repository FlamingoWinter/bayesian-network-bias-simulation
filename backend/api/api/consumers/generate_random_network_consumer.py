import json
from typing import Any

from scipy.stats import rv_discrete

from backend.api.api.cache_network import cache_network_and_generate_candidates
from backend.api.api.consumers.generic_consumer import GenericConsumer
from backend.api.requestTypes.generate_network_request import RandomNetworkRequest, \
    new_generate_network_request
from backend.network.generation.generate_categorical_network import generate_random_categorical_network
from backend.network.pgmpy_network import PgmPyNetwork


class GenerateRandomNetworkConsumer(GenericConsumer):
    session_key: str

    async def receive(self,
                      text_data: Any = None,
                      bytes_data: Any = None) -> None:
        # TODO: Logic if random request is continuous
        request: RandomNetworkRequest = new_generate_network_request(**json.loads(text_data))

        category_number_dist = rv_discrete(
            values=([int(x) for x in request.values_per_variable.keys()],
                    list(request.values_per_variable.values())))

        network: PgmPyNetwork = generate_random_categorical_network(request.number_of_nodes,
                                                                    request.parents_range,
                                                                    request.mutual_information_range,
                                                                    category_number_dist)

        await self.send(text_data=json.dumps({
            'message': f"Network Generation Completed"
        }))

        cache_network_and_generate_candidates(network, self.session_key)

        await self.send(text_data=json.dumps({
            'message': f"Candidate Generation Completed"
        }))

        await self.close(code=1000)
