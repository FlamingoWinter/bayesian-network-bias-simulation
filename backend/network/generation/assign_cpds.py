import math
from itertools import product
from typing import Tuple

import networkx as nx
import numpy as np
from numpy import ndarray
from pgmpy.factors.discrete import TabularCPD

from backend.entropy.entropy import categorical_entropy_of_probabilities


def assign_cpds(model, graph: nx.DiGraph, num_categories_by_node: dict[str, int],
                mutual_information_range: Tuple[float, float] = (0.6, 0.9), alpha: float = 1):
    if alpha < 1e-5:
        raise Exception("Could not assign cpds")

    node_probabilities_by_node: dict[str, dict[int, float]] = {}
    cpds = []

    for node in graph.nodes:
        num_categories = num_categories_by_node[node]
        predecessors = list(graph.predecessors(node))
        num_categories_for_predecessors = [num_categories_by_node[predecessor] for predecessor in predecessors]
        predecessor_values = [list(t) for t in
                              product(*[list(range(num_categories)) for num_categories in
                                        num_categories_for_predecessors])]

        cpd = [generate_categorical_distribution_from_dirichlet(num_categories, 1)]

        if len(predecessors) == 0:
            cpd = [generate_categorical_distribution_from_dirichlet(num_categories, 1)]
            node_probabilities_by_node[node] = calculate_node_probabilities(predecessors, node_probabilities_by_node,
                                                                            cpd, predecessor_values, num_categories)
        else:
            standardised_mutual_information = -1
            attempts = 0
            while not (mutual_information_range[0] <= standardised_mutual_information <= mutual_information_range[1]):
                cpd = [generate_categorical_distribution_from_dirichlet(num_categories, alpha) for _ in
                       predecessor_values]
                node_probabilities_by_node[node] = calculate_node_probabilities(predecessors,
                                                                                node_probabilities_by_node,
                                                                                cpd, predecessor_values, num_categories)
                h_y = categorical_entropy_of_probabilities(np.array(list(node_probabilities_by_node[node].values())))
                h_y_given_predecessors = get_entropy_given_predecessors(predecessors,
                                                                        node_probabilities_by_node,
                                                                        cpd, predecessor_values)
                mutual_information = h_y - h_y_given_predecessors
                max_mutual_information = min(math.log2(num_categories), math.log2(len(predecessor_values)))

                standardised_mutual_information = mutual_information / max_mutual_information

                attempts += 1
                if attempts > 1000:
                    # Network generation might get to a point where no new nodes can be generated with the desired
                    # mutual information. We restart network generation with more dense (higher entropy) distributions.
                    alpha = alpha / 2
                    print(f"Generating cpds failed. Retrying with alpha = {alpha}....")
                    return assign_cpds(model, graph, num_categories_by_node, mutual_information_range, alpha)

        cpds.append(TabularCPD(variable=node, variable_card=num_categories,
                               values=list(zip(*cpd)),
                               evidence=predecessors,
                               evidence_card=num_categories_for_predecessors))

    for cpd in cpds:
        model.add_cpds(cpd)


def calculate_node_probabilities(predecessors_of_node: list[str],
                                 node_probabilities_by_node: dict[str, dict[int, float]],
                                 node_cpd: list[ndarray],
                                 predecessor_values_of_node: list[list],
                                 num_categories_in_node: int,
                                 ) -> dict[int, float]:
    probabilities = {}
    # P(Y=y) = sum_{a,b}( P(A=a) p(B=b) p(C=c|A=a,B=b)  )
    for category in range(num_categories_in_node):
        probabilities[category] = 0

        if len(predecessors_of_node) == 0:
            probabilities[category] = float(node_cpd[0][category])
        else:
            for (predecessor_value_index, predecessor_values) in enumerate(predecessor_values_of_node):
                # cum_prod = p(a) p(b) ...
                cum_prod = 1
                for (predecessor, predecessor_value) in zip(predecessors_of_node, predecessor_values):
                    cum_prod *= node_probabilities_by_node[predecessor][predecessor_value]
                probabilities[category] += cum_prod * node_cpd[predecessor_value_index][
                    category]
    return probabilities


def get_entropy_given_predecessors(predecessors_of_node: list[str],
                                   node_probabilities_by_node: dict[str, dict[int, float]],
                                   node_cpd: list[ndarray],
                                   predecessor_values_of_node: list[list]) -> float:
    # H(Y=y given A=a, B=b) = sum_{a,b}( p(A=a) p(B=b) H(Y=y | A=a, B=b)
    entropy = 0

    for (predecessor_value_index, predecessor_values) in enumerate(predecessor_values_of_node):
        cum_prod = 1
        for (predecessor, predecessor_value) in zip(predecessors_of_node, predecessor_values):
            cum_prod *= node_probabilities_by_node[predecessor][predecessor_value]
        entropy_given_predecessor_values = categorical_entropy_of_probabilities(node_cpd[predecessor_value_index])
        entropy += cum_prod * entropy_given_predecessor_values

    return entropy


def generate_categorical_distribution_from_dirichlet(num_categories: int, alpha: float = 1) -> ndarray:
    return np.random.dirichlet([alpha] * num_categories)
