from typing import Dict

import numpy as np

from backend.network.bayesian_network import BayesianNetwork
from backend.network.example_networks.weighted_coin import get_weighted_coin_network
from backend.utilities.time_function import time_function


@time_function("Generating network")
def generate_network(observed: Dict[str, np.array]) -> BayesianNetwork:
    # TODO: Implement this function.
    #    This is currently returning a placeholder example network, but should return a randomised Bayesian
    #    network which mirrors the dependencies of variables in reality and should be customisable.

    return get_weighted_coin_network(observed)
