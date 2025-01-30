from typing import Dict, Any

import networkx as nx
import numpy as np
from numpy import ndarray, dtype, floating
from numpy._typing import _64Bit
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianNetwork as PgBn

from backend.network.pgmpy_network import PgmPyNetwork


def generate_random_categorical_network_from_nx(graph: nx.DiGraph):
    model = PgBn(ebunch=graph)

    num_categories_by_node: Dict[str, int] = {node: 2 for node in graph.nodes}

    for node in graph.nodes:
        num_categories = num_categories_by_node[node]

        predecessors = list(graph.predecessors(node))
        num_categories_for_predecessors = [num_categories_by_node[predecessor] for predecessor in predecessors]

        values_to_generate = range(int(np.prod(num_categories_for_predecessors)))

        random_values = [generate_categorical_distribution_from_dirichlet(num_categories) for _ in
                         values_to_generate]

        cpd = TabularCPD(variable=node, variable_card=2,
                         values=list(zip(*random_values)),
                         evidence=predecessors,
                         evidence_card=num_categories_for_predecessors)
        model.add_cpds(cpd)

    network = PgmPyNetwork(model)

    for node in graph.nodes:
        network.set_category_names_for_characteristic(node, ["1", '2'])

    network.score_characteristic = list(graph.nodes)[-1]
    network.application_characteristics = list(graph.nodes)[:-1]

    return network


def generate_categorical_distribution_from_dirichlet(num_categories: int) -> ndarray[Any, dtype[floating[_64Bit]]]:
    return np.random.dirichlet([1] * num_categories)
