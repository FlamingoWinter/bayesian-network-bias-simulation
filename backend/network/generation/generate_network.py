from typing import Union, Literal, Tuple

from backend.network.bayesian_network import BayesianNetwork
from backend.network.generation.generate_categorical_network import \
    random_categorical_network_from_nx_with_bounded_mutual_information
from backend.network.generation.generate_dag import generate_random_dag
from backend.utilities.time_function import time_function


@time_function("Generating network")
def generate_network() -> BayesianNetwork:
    # TODO: Implement this function.
    #    This is currently returning a placeholder example network, but should return a randomised Bayesian
    #    network which mirrors the dependencies of variables in reality and should be customisable.

    # return get_asia_network()
    return generate_random_network(10)


def generate_random_network(number_of_nodes,
                            parents: Tuple[int, int] = (2, 3),
                            mutual_information: Tuple[float, float] = (0.6, 0.9)
                            ):
    categorical_or_continuous: Union[Literal["categorical"], Literal["continuous"]]

    graph = generate_random_dag(number_of_nodes, parents[0], parents[1])
    return random_categorical_network_from_nx_with_bounded_mutual_information(graph, mutual_information[0],
                                                                              mutual_information[1])
