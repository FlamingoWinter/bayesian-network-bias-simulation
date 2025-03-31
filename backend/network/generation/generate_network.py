from typing import Union, Literal

from backend.network.bayesian_network import BayesianNetwork
from backend.network.generation.generate_categorical_network import \
    generate_random_categorical_network
from backend.utilities.time_function import time_function


@time_function("Generating network")
def generate_network() -> BayesianNetwork:
    # TODO: Implement this function.
    #    This is currently returning a placeholder example network, but should return a randomised Bayesian
    #    network which mirrors the dependencies of variables in reality and should be customisable.

    return generate_random_network()


def generate_random_network():
    categorical_or_continuous: Union[Literal["categorical"], Literal["continuous"]]

    return generate_random_categorical_network(15)
