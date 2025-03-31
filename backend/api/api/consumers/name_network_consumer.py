from typing import Any, cast

from backend.api.api.cache_network import cache_network_and_generate_candidates, get_network_from_cache
from backend.api.api.consumers.generic_consumer import GenericConsumer
from backend.network.bayesian_network import BayesianNetwork
from backend.network.naming_characteristics.name_characteristics import name_characteristics
from backend.network.pgmpy_network import PgmPyNetwork


class NameNetworkConsumer(GenericConsumer):
    session_key: str

    async def receive(self,
                      text_data: Any = None,
                      bytes_data: Any = None) -> None:
        network: BayesianNetwork = get_network_from_cache(self.session_key)

        if network.model_type == "pgmpy":
            network: PgmPyNetwork = cast(PgmPyNetwork, network)
            network = name_characteristics(network)

            await self.send_and_flush(f"Network Renaming Completed")

            cache_network_and_generate_candidates(network, self.session_key)

            await self.send_and_flush(f"Candidate Generation Completed")
        else:
            await self.send_and_flush("Error: Network is not a categorical one.", error=True)

        await self.close(code=1000)
