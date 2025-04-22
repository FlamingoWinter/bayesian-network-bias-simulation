import random
from typing import Tuple

from pgmpy.models import BayesianNetwork as PgBn
from scipy.stats import rv_discrete

from backend.network.generation.assign_cpds import assign_cpds
from backend.network.generation.choose_characteristics import choose_score, choose_application
from backend.network.generation.generate_dag import generate_random_dag
from backend.network.pgmpy_network import PgmPyNetwork

default_category_number_dist = rv_discrete(values=([2, 3, 4], [0.6, 0.3, 0.1]))


def generate_random_categorical_network(nodes: int = 50, parents_range: Tuple[int, int] = (2, 3),
                                        mutual_information_range: Tuple[float, float] = (0.6, 0.9),
                                        category_number_dist=None, seed=None) -> PgmPyNetwork:
    if category_number_dist is None:
        category_number_dist = rv_discrete(values=([2, 3, 4], [0.6, 0.3, 0.1]))

    if seed:
        random.seed(seed)

    graph = generate_random_dag(nodes, parents_range)
    num_categories_by_node: dict[str, int] = {node: category_number_dist.rvs() for node in list(graph.nodes)}

    score_characteristic = choose_score(graph)
    num_categories_by_node[score_characteristic] = 2

    model = PgBn(ebunch=graph)
    assign_cpds(model, graph, num_categories_by_node, mutual_information_range)

    network: PgmPyNetwork = PgmPyNetwork(model)

    for node in graph.nodes:
        network.set_category_names_for_characteristic(node, [str(x) for x in
                                                             list(range(1, num_categories_by_node[node] + 1))])

    network.score_characteristic = score_characteristic
    network.application_characteristics = choose_application(graph, 1, score_characteristic)

    network.predefined = False

    return network
