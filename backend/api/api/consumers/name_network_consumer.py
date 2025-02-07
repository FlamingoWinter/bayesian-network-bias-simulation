import json
from typing import Any
from urllib.parse import parse_qs

import pymc as pm
from channels.generic.websocket import AsyncWebsocketConsumer
from pgmpy.models import BayesianNetwork as PgBn

from backend.api.api.cache_network import cache_network
from backend.api.cache.cache import from_cache
from backend.network.bayesian_network import BayesianNetwork
from backend.network.naming_characteristics.name_characteristics import name_characteristics


class NameNetworkConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope.get("query_string", b"").decode("utf-8")

        query_params = parse_qs(query_string)
        self.session_key = query_params.get("session_key", [None])[0]

        self.room_name = "new-network"

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self,
                      text_data: Any = None,
                      bytes_data: Any = None) -> None:
        network: BayesianNetwork = from_cache(f"network_{self.session_key}",
                                              "network")
        if network.model_type == "pgmpy":
            network.model.__class__ = PgBn
        else:
            network.model.__class__ = pm.Model

        if network.model_type == "pgmpy":
            network = name_characteristics(network)

            await self.send(text_data=json.dumps({
                'message': f"Network Renaming Completed"
            }))

            cache_network(network, self.session_key)

            await self.send(text_data=json.dumps({
                'message': f"Candidate Generation Completed"
            }))
        else:
            await self.send(text_data=json.dumps({
                'message': f"Error: Network is not a categorical one.",
                'error': 'true'
            }))

        await self.close(code=1000)
