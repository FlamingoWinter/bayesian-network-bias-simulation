import math
import random
from itertools import islice
from typing import Dict, Union, Literal, List

import networkx as nx
import numpy as np
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianNetwork as PgBn

from backend.network.bayesian_network import BayesianNetwork
from backend.network.pgmpy_network import PgmPyNetwork
from backend.utilities.time_function import time_function


@time_function("Generating network")
def generate_network(observed: Dict[str, np.array]) -> BayesianNetwork:
    # TODO: Implement this function.
    #    This is currently returning a placeholder example network, but should return a randomised Bayesian
    #    network which mirrors the dependencies of variables in reality and should be customisable.

    return generate_random_network(10, 2, 3)


def generate_random_network(number_of_nodes, min_parents: int, max_parents: int):
    categorical_or_continuous: Union[Literal["categorical"], Literal["continuous"]]
    average_dependency: float
    dependency_variance: float

    graph = generate_random_dag(number_of_nodes, 1, 2)
    return primitive_pgmpy_from_nx(graph)


def primitive_pgmpy_from_nx(graph: nx.DiGraph):
    "This generates a pgmpy model with completely random probabilities from an nx model. Mostly for testing purposes."
    print(graph)

    model = PgBn(ebunch=graph)

    for node in graph.nodes:
        predecessors = list(graph.predecessors(node))
        predecessor_count = len(predecessors)
        values_to_generate = range(2 ** predecessor_count)

        random_values = [random.uniform(0, 1) for _ in values_to_generate]

        cpd = TabularCPD(variable=node, variable_card=2,
                         values=[[1 - x for x in random_values],
                                 [x for x in random_values]],
                         evidence=predecessors,
                         evidence_card=[2 for _ in range(predecessor_count)])
        model.add_cpds(cpd)

    network = PgmPyNetwork(model)

    for node in graph.nodes:
        network.set_category_names_for_characteristic(node, ["1", '2'])

    return network


def generate_random_unconnected_dag_gnp(connectedness: float, nodes: int):
    directed_graph = nx.gnp_random_graph(nodes, connectedness, directed=True)
    directed_acyclic_graph = nx.DiGraph([(u, v) for (u, v) in directed_graph.edges() if u < v])

    return nx.relabel_nodes(directed_acyclic_graph, {node: str(node) for node in list(directed_acyclic_graph.nodes)})


@time_function("Generate random dag")
def generate_random_dag(nodes: int, min_parents: int, max_parents: int) -> nx.DiGraph:
    # We want a random item out of the space of all connected directed acyclic graphs.

    # The difficulty with approaches to generating "random" directed acyclic graphs is that while
    # they're often generated to be unpredictable, they're rarely generated truly randomly.
    # (i.e.- such that each graph has an equal chance to be chosen).

    # We don't want bias in network structure affecting any results, so we generate them at random uniformly
    # from the collection of all connected directed acyclic graphs.
    # Unfortunately, this is difficult, as discussed below.
    # https://link.springer.com/article/10.1007/s11222-013-9428-y#Sec6
    # We adapt the algorithm given in this paper for our use case.

    # The basic strategy is to determine some ordering or enumeration of all directed acyclic graphs and to sample
    # uniformly from this enumeration.

    while True:
        point_names = iter(range(nodes))
        # We sample from the enumeration of all graphs to determine the number of out-points our graph
        # should have in each layer.
        # Randomly sampling a graph given these values is trivial.
        out_point_counts = calculate_out_point_counts(nodes, min_parents, max_parents)

        dag = nx.DiGraph()

        # Create first out points
        out_points = list(islice(point_names, out_point_counts[-1]))
        dag.add_nodes_from(out_points)

        # Build each successive layer of out_points
        for out_point_count in reversed(out_point_counts[:-1]):
            out_points = list(islice(point_names, out_point_count))
            node_list = list(dag.nodes)
            random.shuffle(node_list)

            dag.add_nodes_from(out_points)
            for out_point in out_points:
                while True:
                    connections = np.random.binomial(n=len(node_list), p=0.5)
                    if min_parents <= connections <= max_parents:
                        break

                for node in node_list[:connections]:
                    dag.add_edge(node, out_point)

        if nx.is_weakly_connected:
            break

    return nx.relabel_nodes(dag, {node: str(node) for node in list(dag.nodes)})


def calculate_out_point_counts(nodes: int, min_parents: int, max_parents: int) -> List[int]:
    # An out-node is a node with no direct parents.
    # The enumeration considers that each DAG can be described by its out-points,
    # their connections and other smaller DAGs. To list all DAGs it is sufficient to
    # list them in order of the number of out-points on each layer.

    # For a given number of nodes, by determining the number of DAGs with each number of out-points,
    # we can then sample that uniformly to determine the number of out-points our DAG should have.
    # We repeat the process, to construct a list of desired numbers of out-points.
    # Once we have those numbers, it is trivial to construct a random DAG

    # This algorithm differs from the one in
    # https://link.springer.com/article/10.1007/s11222-013-9428-y#Sec6
    # because we do not consider permutations. For our purposes, the permutation of node labels in a graph
    # will be considered to be the same graph. So we've removed the combinatorial coefficient
    # for relabelling nodes.

    # Next, we use the variation with a minimum and maximum number of parents.

    def frequency_dag_with_m_nodes_and_s_outpoints_appears_in_dag_with_k_outpoints(m, s, k):
        # For any dag with m nodes and s outpoints, returns the number of dags which
        # exist with k outpoints for which removing the first layer of outpoints leaves us with the dag.
        if min_parents == 1 and max_parents > k:
            ways_outpoints_can_be_connected = 2 ** k
        else:
            # https://link.springer.com/article/10.1007/s11222-013-9428-y#Equ21
            ways_outpoints_can_be_connected = 0
            for i in range(max(1, min_parents), min(max_parents, k) + 1):
                ways_outpoints_can_be_connected += math.comb(k, i)

        # each of the s old outpoints must have at least one connection, or else it would be on the same outpoint-level
        # as the k outpoints we are adding.
        # so we subtract the case where they have no connections.
        return (ways_outpoints_can_be_connected - 1) ** s * ways_outpoints_can_be_connected ** (m - s)

    # a[n, k] is how many graphs there are with n nodes and k out-points, ignoring permutations.
    a = np.ones((nodes + 1, nodes + 1), dtype=object)

    for n in range(1, nodes + 1):
        for k in range(1, n + 1):
            m = n - k

            if m != 0:
                # m is the number of nodes in the hypothetical DAG with the k out-points removed.
                # if that number is zero, then for DP purposes it is still useful to consider that there exists
                # "one" empty graph.

                # Otherwise, we initialise b to 0 as we will be building this recursively.
                a[n, k] = 0

            for s in range(1, m + 1):
                # We add to a[n,k] the number of dags with m nodes and s out-points,
                # multiplied by how many times each appears in a DAG with n nodes and k-outpoints
                a[n, k] += a[m, s] * frequency_dag_with_m_nodes_and_s_outpoints_appears_in_dag_with_k_outpoints(m, s, k)

    a[0, :] = 0
    a[:, 0] = 0

    a_n = np.sum(a[-1])

    r = random.randint(1, a_n)

    nodes_remaining = nodes
    out_point_counts = []

    # First iteration
    out_points = 1
    while r > a[nodes_remaining][out_points]:
        r -= a[nodes_remaining][out_points]
        out_points += 1

    out_point_counts.append(out_points)
    nodes_remaining -= out_points
    old_out_points = out_points

    # Nth iteration
    while nodes_remaining > 0:
        out_points = 1

        while True:
            scaling_factor = (
                frequency_dag_with_m_nodes_and_s_outpoints_appears_in_dag_with_k_outpoints(m=nodes_remaining,
                                                                                           s=out_points,
                                                                                           k=old_out_points))
            next_to_remove = scaling_factor * a[nodes_remaining, out_points]
            if r < next_to_remove:
                r //= scaling_factor
                out_point_counts.append(out_points)
                nodes_remaining -= out_points
                old_out_points = out_points
                break

            r -= next_to_remove
            out_points += 1

    return out_point_counts


if __name__ == "__main__":
    generate_random_dag(10)
