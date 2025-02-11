import json
from typing import Any
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer
from scipy.stats import rv_discrete

from backend.api.api.cache_network import cache_network
from backend.api.requestTypes.generateNetworkRequest import CategoricalNetworkRequest
from backend.network.generation.generate_categorical_network import generate_random_categorical_network
from backend.network.pgmpy_network import PgmPyNetwork


class GenerateNetworkConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope.get("query_string", b"").decode("utf-8")

        query_params = parse_qs(query_string)
        self.session_key = query_params.get("session_key", [None])[0]

        self.room_name = "generate-network"

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self,
                      text_data: Any = None,
                      bytes_data: Any = None) -> None:
        # TODO: This shouldn't work for just categorical network requests
        generate_network_request = CategoricalNetworkRequest(**json.loads(text_data))

        parents = (generate_network_request.min_allowed_parents, generate_network_request.max_allowed_parents)
        mutual_information = (generate_network_request.min_allowed_mutual_information,
                              generate_network_request.max_allowed_mutual_information)

        category_number_dist = rv_discrete(
            values=([int(x) for x in generate_network_request.values_per_variable.keys()],
                    list(generate_network_request.values_per_variable.values())))

        network: PgmPyNetwork = generate_random_categorical_network(generate_network_request.number_of_nodes,
                                                                    parents,
                                                                    mutual_information,
                                                                    category_number_dist
                                                                    )

        await self.send(text_data=json.dumps({
            'message': f"Network Generation Completed"
        }))

        cache_network(network, self.session_key)

        await self.send(text_data=json.dumps({
            'message': f"Candidate Generation Completed"
        }))

        await self.close(code=1000)
