import pymc as pm
from pgmpy.models import BayesianNetwork as PgBn

from backend.api.cache.cache import cache, from_cache
from backend.api.responseTypes.networkResponse import NetworkResponse
from backend.candidates.candidate_group import CandidateGroup
from backend.candidates.generate_candidates import generate_candidate_group
from backend.network.bayesian_network import BayesianNetwork, num_samples


def cache_network_and_generate_candidates(network: BayesianNetwork, session_id: str = None):
    network_response: NetworkResponse = network.to_network_response()

    candidate_group: CandidateGroup = generate_candidate_group(network, num_samples)

    for characteristic in network.characteristics:
        network_response["characteristics"][characteristic]["priorDistribution"] \
            = candidate_group.characteristic_to_distribution(characteristic)

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
