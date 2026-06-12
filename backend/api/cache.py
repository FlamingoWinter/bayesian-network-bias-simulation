from typing import Any, Optional

import dill
from django.core.cache import cache as django_cache
from pgmpy.models import BayesianNetwork as PgBn

from backend.api.schemas import NetworkResponse
from backend.simulation.build_network.bayesian_network import BayesianNetwork


def cache(key: str, to_cache):
    django_cache.set(key, dill.dumps(to_cache), timeout=None)


def from_cache(key: str, backup_key: str = "") -> Any:
    try:
        return dill.loads(django_cache.get(key))
    except Exception:
        print("used backup instead of", key)
        return dill.loads(django_cache.get(backup_key))


def cache_network_and_generate_applicants(
    network: BayesianNetwork, session_id: Optional[str] = None
):
    network_response: NetworkResponse = network.to_network_response()

    if session_id is not None:
        cache(f"network_{session_id}", network)
        cache(f"network-response_{session_id}", network_response)
    else:
        cache("network", network)
        cache("network-response", network_response)


def get_network_from_cache(session_key: str) -> BayesianNetwork:
    network: BayesianNetwork = from_cache(f"network_{session_key}", "network")
    network.model.__class__ = PgBn
    return network
