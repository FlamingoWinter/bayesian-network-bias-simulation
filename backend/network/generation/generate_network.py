from typing import Union, Literal

from backend.network.bayesian_network import BayesianNetwork
from backend.network.generation.generate_categorical_network import generate_random_categorical_network_from_nx
from backend.network.generation.generate_dag import generate_random_dag
from backend.utilities.time_function import time_function


@time_function("Generating network")
def generate_network() -> BayesianNetwork:
    # TODO: Implement this function.
    #    This is currently returning a placeholder example network, but should return a randomised Bayesian
    #    network which mirrors the dependencies of variables in reality and should be customisable.

    # return get_asia_network()
    return generate_random_network(10, 2, 3)


def generate_random_network(number_of_nodes, min_parents: int, max_parents: int):
    categorical_or_continuous: Union[Literal["categorical"], Literal["continuous"]]
    average_dependency: float
    dependency_variance: float

    graph = generate_random_dag(number_of_nodes, min_parents, max_parents)
    return generate_random_categorical_network_from_nx(graph)
