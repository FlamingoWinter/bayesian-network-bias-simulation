from backend.network.bayesian_network import BayesianNetwork
from backend.network.example_networks.asia import get_asia_network
from backend.utilities.time_function import time_function


@time_function("Generating network")
def generate_network() -> BayesianNetwork:
    # TODO: Implement this function.
    #    This is currently returning a placeholder example network, but should return a randomised Bayesian
    #    network which mirrors the dependencies of variables in reality and should be customisable.

    return get_asia_network()
