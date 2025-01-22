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

    return generate_random_network()


def generate_random_network():
    categorical_or_continuous: Union[Literal["categorical"], Literal["continuous"]]
    average_dependency: float
    dependency_variance: float
    number_of_nodes: int = 10
    graph_connectedness: float = 0.1

    graph = generate_random_dag(number_of_nodes)
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
def generate_random_dag(nodes: int) -> nx.DiGraph:
    # We want a random item out of the space of all connected directed acyclic graphs.

    # The difficulty with approaches to generating "random" directed acyclic graphs is that while
    # they're often generated to be unpredictable, they're really generated truly randomly.

    # We don't want bias in network structure affecting any results, so we generate them at random uniformly
    # from the collection of all connected directed acyclic graphs.
    # Unfortunately, this is difficult as discussed below.

    # https://link.springer.com/article/10.1007/s11222-013-9428-y#Sec6

    # The basic strategy is to determine some ordering or enumeration of all directed acyclic graphs and to sample
    # uniformly from this enumeration.

    while True:
        point_names = iter(range(nodes))
        out_point_counts = calculate_out_point_counts(nodes)

        dag = nx.DiGraph()

        # Create first out points
        out_points = list(islice(point_names, out_point_counts[-1]))
        dag.add_nodes_from(out_points)

        for out_point_count in reversed(out_point_counts[:-1]):
            out_points = list(islice(point_names, out_point_count))
            node_list = list(dag.nodes)
            dag.add_nodes_from(out_points)
            for out_point in out_points:
                for node in node_list:
                    if random.randint(0, 1) == 0:
                        dag.add_edge(node, out_point)

        if nx.is_weakly_connected:
            break

    return nx.relabel_nodes(dag, {node: str(node) for node in list(dag.nodes)})


def calculate_out_point_counts(nodes: int) -> List[int]:
    # An out-node is a node with no direct parents.
    # The enumeration works by considering that each DAG can be described by its out-nodes,
    # their connections and another smaller DAG.

    # For a given number of nodes, by determining the number of DAGs with each number of out-nodes,
    # we can then sample that uniformly to determine the number of out-nodes our DAG should have.
    # We repeat the process, to construct a list of desired numbers of out-nodes.
    # Once we have those numbers, it is trivial to construct a random DAG

    # a[n][k] is how many graphs there are with n nodes and k out-nodes.
    a = np.ones((nodes + 1, nodes + 1), dtype=object)

    # b[n][k] is how many graphs there are with n nodes and k out-nodes, ignoring permutations.
    b = np.ones((nodes + 1, nodes + 1), dtype=object)

    for n in range(1, nodes + 1):
        for k in range(1, n + 1):
            m = n - k

            if m != 0:
                # m is the number of nodes in the hypothetical DAG with the k out-nodes removed.
                # if that number is zero, then for DP purposes it is still useful to consider that there exists
                # "one" empty graph.

                # Otherwise, we initialise b to 0 as we will be building this recursively.
                b[n, k] = 0

            for s in range(1, m + 1):
                b[n, k] += ((2 ** k - 1) ** s) * (2 ** (k * (m - s))) * a[m, s]

            a[n, k] = math.comb(n, k) * b[n, k]

    a[0, :] = 0
    a[:, 0] = 0

    a_n = np.sum(a[-1])

    r = random.randint(1, a_n)

    nodes_remaining = nodes
    out_node_counts = []

    # First iteration
    out_nodes = 1
    while r > a[nodes_remaining][out_nodes]:
        r -= a[nodes_remaining][out_nodes]
        out_nodes += 1

    r //= math.comb(nodes_remaining, out_nodes)
    out_node_counts.append(out_nodes)
    nodes_remaining -= out_nodes
    old_out_nodes = out_nodes

    # Nth iteration
    while nodes_remaining > 0:
        out_nodes = 1

        while True:
            scaling_factor = ((2 ** old_out_nodes - 1) ** out_nodes) * (
                    2 ** (old_out_nodes * (nodes_remaining - out_nodes)))
            next_to_remove = scaling_factor * a[nodes_remaining, out_nodes]
            if r < next_to_remove:
                r //= math.comb(nodes_remaining, out_nodes)
                r //= scaling_factor
                out_node_counts.append(out_nodes)
                nodes_remaining -= out_nodes
                old_out_nodes = out_nodes
                break

            r -= next_to_remove
            out_nodes += 1

    return out_node_counts


if __name__ == "__main__":
    generate_random_dag(10)
