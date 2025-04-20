import math
import random
from itertools import product
from typing import Any, Tuple

import networkx as nx
import numpy as np
from numpy import ndarray, dtype, floating
from numpy._typing import _64Bit
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianNetwork as PgBn
from scipy.stats import rv_discrete

from backend.entropy.entropy import categorical_entropy
from backend.network.bayesian_network import BayesianNetwork
from backend.network.generation.generate_dag import generate_random_dag
from backend.network.pgmpy_network import PgmPyNetwork

default_category_number_dist = rv_discrete(values=([2, 3, 4], [0.6, 0.3, 0.1]))


def generate_random_categorical_network(nodes: int = 50, parents_range: Tuple[int, int] = (2, 3),
                                        mutual_information_range: Tuple[float, float] = (0.6, 0.9),
                                        category_number_dist=None, seed=None) -> BayesianNetwork:
    if seed:
        random.seed(seed)

    if category_number_dist is None:
        category_number_dist = rv_discrete(values=([2, 3, 4], [0.6, 0.3, 0.1]))

    graph = generate_random_dag(nodes, parents_range[0], parents_range[1])
    num_categories_by_node: dict[str, int] = {node: category_number_dist.rvs() for node in graph.nodes}

    score_characteristic = choose_score_characteristic(graph)
    num_categories_by_node[score_characteristic] = 2

    model = PgBn(ebunch=graph)
    assign_cpds(model, graph, num_categories_by_node, mutual_information_range)

    network: BayesianNetwork = PgmPyNetwork(model)

    for node in graph.nodes:
        network.set_category_names_for_characteristic(node, [str(x) for x in
                                                             list(range(1, num_categories_by_node[node] + 1))])

    network.score_characteristic = score_characteristic
    network.application_characteristics = choose_application_characteristics(graph, score_characteristic)

    network.predefined = False

    return network


def choose_score_characteristic(graph: nx.DiGraph) -> str:
    nodes_without_ancestors = [node for node, deg in graph.in_degree() if deg == 0]
    direct_children = list(set([child for p in nodes_without_ancestors for child in graph.successors(p)]))
    direct_grandchildren = list(set([child for p in direct_children for child in graph.successors(p)]))

    score_non_candidates = set(nodes_without_ancestors + direct_children + direct_grandchildren)
    score_candidates = [node for node in graph.nodes if node not in score_non_candidates]

    for candidate in score_candidates:
        descendants = nx.descendants(graph, candidate)

    if len(score_candidates) == 0:
        score_characteristic = list(graph.nodes)[-1]
    else:
        score_characteristic = random.sample(score_candidates, 1)[0]
    return score_characteristic


def choose_application_characteristics(graph: nx.DiGraph, score_characteristic: str):
    score_descendants = list(nx.descendants(graph, score_characteristic))
    score_direct_parents = list(graph.predecessors(score_characteristic))

    all_nodes = set(graph.nodes)
    connected_nodes = set(score_descendants + score_direct_parents + [score_characteristic])
    unconnected_nodes = list(all_nodes - connected_nodes)

    return random.sample(unconnected_nodes, len(unconnected_nodes) // 2)


def assign_cpds(model, graph: nx.DiGraph, num_categories_by_node: dict[str, int],
                mutual_information_range: Tuple[float, float] = (0.6, 0.9), alpha: float = 1):
    if alpha < 1e-5:
        raise "Could not assign cpds"
    node_probabilities: dict[str, dict[int, float]] = {}
    cpds = []
    for node in graph.nodes:
        num_categories = num_categories_by_node[node]
        predecessors = list(graph.predecessors(node))
        num_categories_for_predecessors = [num_categories_by_node[predecessor] for predecessor in predecessors]
        predecessor_values_list = [list(t) for t in
                                   product(*[list(range(num_categories)) for num_categories in
                                             num_categories_for_predecessors])]

        def calculate_node_probability() -> dict[int, float]:
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

        cpd = [generate_categorical_distribution_from_dirichlet(num_categories, 1)]
        if len(predecessors) == 0:
            cpd = [generate_categorical_distribution_from_dirichlet(num_categories, 1)]
            node_probabilities[node] = calculate_node_probability()
        else:
            standardised_mutual_information = -1
            attempts = 0
            while not (mutual_information_range[0] <= standardised_mutual_information <= mutual_information_range[1]):
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
                    # mutual information. In this case, we just restart network generation with more dense (higher entropy) distributions.
                    alpha = alpha / 2
                    print(f"Generating cpds failed. Retrying with alpha = {alpha}....")
                    return assign_cpds(model, graph, num_categories_by_node, mutual_information_range, alpha)
        cpds.append(TabularCPD(variable=node, variable_card=num_categories,
                               values=list(zip(*cpd)),
                               evidence=predecessors,
                               evidence_card=num_categories_for_predecessors))
    for cpd in cpds:
        model.add_cpds(cpd)


def generate_categorical_distribution_from_dirichlet(num_categories: int, alpha: float = 1) -> ndarray[
    Any, dtype[floating[_64Bit]]]:
    return np.random.dirichlet([alpha] * num_categories)
