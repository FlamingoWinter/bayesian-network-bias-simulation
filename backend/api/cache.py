from typing import Any

import dill
import pymc as pm
from django.core.cache import cache as django_cache
from pgmpy.models import BayesianNetwork as PgBn

from backend.api.responseTypes.network_response import NetworkResponse
from backend.network.bayesian_network import BayesianNetwork


def cache(key: str, to_cache):
    django_cache.set(key, dill.dumps(to_cache), timeout=None)


def from_cache(key: str, backup_key: str = "") -> Any:
    try:
        return dill.loads(django_cache.get(key))
    except:
        print("used backup instead of", key)
        return dill.loads(django_cache.get(backup_key))


def cache_network_and_generate_applicants(network: BayesianNetwork, session_id: str = None):
    network_response: NetworkResponse = network.to_network_response()

    if session_id is not None:
        cache(f"network_{session_id}", network)
        cache(f"network-response_{session_id}", network_response)
    else:
        cache(f"network", network)
        cache(f"network-response", network_response)


def get_network_from_cache(session_key: str) -> BayesianNetwork:
    network: BayesianNetwork = from_cache(f"network_{session_key}",
                                          "network")
    if network.model_type == "pgmpy":
        network.model.__class__ = PgBn
    else:
        network.model.__class__ = pm.Model

    return network
