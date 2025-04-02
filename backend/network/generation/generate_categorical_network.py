import math
import random
from itertools import product
from typing import Dict, Any, Tuple, Literal, Union

import networkx as nx
import numpy as np
from numpy import ndarray, dtype, floating
from numpy._typing import _64Bit
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianNetwork as PgBn
from scipy.stats import rv_discrete

from backend.entropy.entropy import categorical_entropy
from backend.network.generation.generate_dag import generate_random_dag
from backend.network.pgmpy_network import PgmPyNetwork

default_category_number_dist = rv_discrete(values=([2, 3, 4], [0.6, 0.3, 0.1]))


def generate_random_categorical_network(nodes: int,
                                        parents_range: Tuple[int, int] = (2, 3),
                                        mutual_information_range: Tuple[float, float] = (0.6, 0.9),
                                        category_numbers: rv_discrete = default_category_number_dist
                                        ):
    categorical_or_continuous: Union[Literal["categorical"], Literal["continuous"]]

    graph = generate_random_dag(nodes, parents_range[0], parents_range[1])
    return random_categorical_network_from_nx_with_bounded_mutual_information(graph, mutual_information_range[0],
                                                                              mutual_information_range[1],
                                                                              category_numbers)


def random_categorical_network_from_nx_with_bounded_mutual_information(graph: nx.DiGraph,
                                                                       left: float,
                                                                       right: float,
                                                                       category_numbers_dist: rv_discrete,
                                                                       alpha: float = 1
                                                                       ):
    # We're placing a bound on the mutual information between each variable and its set of parents.

    # Alpha is how concentrated the Dirichlets are. If the network fails to generate
    # (because generating values with suitable mutual information are too difficult),
    # then alpha can be reduced.

    if not (0 <= left <= 1) or not (0 <= right <= 1):
        raise Exception("Make sure left and right are between 0 and 1")
    if right - left < 0.1:
        raise Exception("Make the distance between left and right bigger")

    model = PgBn(ebunch=graph)

    num_categories_by_node: Dict[str, int] = {node: category_numbers_dist.rvs() for node in graph.nodes}

    # Ensure the score node is 2-valued.

    # The score characteristic can be any node which isn't a child or grandchild of an in-node
    nodes_without_ancestors = [node for node, deg in graph.in_degree() if deg == 0]
    direct_children = list(set([child for p in nodes_without_ancestors for child in graph.successors(p)]))
    direct_grandchildren = list(set([child for p in direct_children for child in graph.successors(p)]))

    score_non_candidates = set(nodes_without_ancestors + direct_children + direct_grandchildren)
    score_candidates = [node for node in graph.nodes if node not in score_non_candidates]

    if len(score_candidates) == 0:
        score_characteristic = list(graph.nodes)[-1]
    else:
        score_characteristic = random.sample(score_candidates, 1)[0]
    num_categories_by_node[score_characteristic] = 2

    node_probabilities: Dict[str, Dict[int, float]] = {}

    for node in graph.nodes:
        num_categories = num_categories_by_node[node]
        predecessors = list(graph.predecessors(node))
        num_categories_for_predecessors = [num_categories_by_node[predecessor] for predecessor in predecessors]
        predecessor_values_list = [list(t) for t in
                                   product(*[list(range(num_categories)) for num_categories in
                                             num_categories_for_predecessors])]

        def calculate_node_probability() -> Dict[int, float]:
            probabilities = {}
            # p(c) = sum_(a,b)( p(a) p(b) p(c|a,b)  )
            for category in range(num_categories):
                probabilities[category] = 0

                if len(predecessors) == 0:
                    probabilities[category] = float(cpd[0][category])
                else:
                    for (predecessor_value_index, predecessor_values) in enumerate(predecessor_values_list):
                        # cum_prod = p(a) p(b) ...
                        cum_prod = 1
                        for (predecessor, predecessor_value) in zip(predecessors, predecessor_values):
                            cum_prod *= node_probabilities[predecessor][predecessor_value]
                        probabilities[category] += cum_prod * cpd[predecessor_value_index][
                            category]
            return probabilities

        def get_entropy_given_predecessors() -> float:
            # H(y given X) = sum_x( p(x) H(y given X=x)  )
            # H(Y given A, B) = sum_a,b( p(a) p(b) H(Y with a,b)
            entropy = 0

            # We assume there is at least one predecessor
            for (predecessor_value_index, predecessor_values) in enumerate(predecessor_values_list):
                # cum_prod = p(A) p(B) ...
                cum_prod = 1
                for (predecessor, predecessor_value) in zip(predecessors, predecessor_values):
                    cum_prod *= node_probabilities[predecessor][predecessor_value]
                entropy_given_predecessor_values = categorical_entropy(cpd[predecessor_value_index])
                entropy += cum_prod * entropy_given_predecessor_values

            return entropy

        if len(predecessors) == 0:
            cpd = [generate_categorical_distribution_from_dirichlet(num_categories, 1)]
            node_probabilities[node] = calculate_node_probability()
        else:
            standardised_mutual_information = -1
            attempts = 0
            while not (left <= standardised_mutual_information <= right):
                cpd = [generate_categorical_distribution_from_dirichlet(num_categories, alpha) for _ in
                       predecessor_values_list]
                node_probabilities[node] = calculate_node_probability()

                h_y = categorical_entropy(list(node_probabilities[node].values()))
                h_y_given_predecessors = get_entropy_given_predecessors()
                mutual_information = h_y - h_y_given_predecessors
                max_mutual_information = min(math.log2(num_categories), math.log2(len(predecessor_values_list)))

                standardised_mutual_information = mutual_information / max_mutual_information

                attempts += 1
                if attempts > 1000:
                    # Network generation might get to a point where no new nodes can be generated with the desired
                    # mutual information. In this case, we just restart network generation with more dense (higher entropy distributions).
                    alpha = alpha / 2
                    print(f"Generating cpds failed. Retrying with alpha = {alpha}....")
                    return random_categorical_network_from_nx_with_bounded_mutual_information(graph, left, right,
                                                                                              category_numbers_dist,
                                                                                              alpha)

        cpd = TabularCPD(variable=node, variable_card=num_categories,
                         values=list(zip(*cpd)),
                         evidence=predecessors,
                         evidence_card=num_categories_for_predecessors)
        model.add_cpds(cpd)

    network = PgmPyNetwork(model)

    for node in graph.nodes:
        network.set_category_names_for_characteristic(node, [str(x) for x in
                                                             list(range(1, num_categories_by_node[node] + 1))])

    network.score_characteristic = score_characteristic

    # We arbitrarily set the application characteristics to be the direct
    # parents and descendants of the score characteristic

    score_descendants = list(nx.descendants(graph, score_characteristic))
    score_direct_parents = list(graph.predecessors(score_characteristic))

    all_nodes = set(graph.nodes)
    connected_nodes = set(score_descendants + score_direct_parents + [score_characteristic])
    unconnected_nodes = list(all_nodes - connected_nodes)

    network.application_characteristics = random.sample(unconnected_nodes, len(unconnected_nodes) // 2)

    # network.application_characteristics = score_descendants + score_direct_parents

    network.predefined = False

    return network


def random_categorical_network_from_nx(graph: nx.DiGraph,
                                       category_numbers_dist: rv_discrete):
    return random_categorical_network_from_nx_with_bounded_mutual_information(graph, 0, 1, 1, category_numbers_dist)


def generate_categorical_distribution_from_dirichlet(num_categories: int, alpha: float = 1) -> ndarray[
    Any, dtype[floating[_64Bit]]]:
    return np.random.dirichlet([alpha] * num_categories)
