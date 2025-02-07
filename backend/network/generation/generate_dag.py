import math
import random
from itertools import islice
from typing import List

import networkx as nx
import numpy as np

from backend.utilities.time_function import time_function


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
            old_out_points = out_points
            out_points = list(islice(point_names, out_point_count))
            node_list = list(dag.nodes)

            dag.add_nodes_from(out_points)
            # At each layer, we want to randomly connect out-points but need to ensure two things.
            # - Each outpoint has between its minimum and maximum number of parents.
            # - Each previous outpoint is now connected (or it would be an outpoint on this level).

            # We make the second requirement true first by connecting each old outpoint to a new outpoint.
            # We make the first requirement true by selecting some connections value

            connections_by_out_point = {out_point: 0 for out_point in out_points}

            for old_out_point in old_out_points:
                tried = 0
                while True:
                    random_out_point = random.choice(out_points)
                    tried += 1
                    if connections_by_out_point[random_out_point] < max_parents:
                        break
                    if tried > 100:
                        print("failed linking old outpoints")
                dag.add_edge(old_out_point, random_out_point)
                connections_by_out_point[random_out_point] += 1

            for out_point in out_points:
                random.shuffle(node_list)
                tried = 0
                while True:
                    connections = np.random.binomial(n=len(node_list), p=0.5)
                    if max(min_parents, connections_by_out_point[out_point]) <= connections <= max_parents:
                        break
                    tried += 1
                    if tried > 100:
                        print("failed generating connections within min_parents and max_parents")
                        break

                for node in node_list[:(connections - connections_by_out_point[out_point])]:
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

    # https://link.springer.com/article/10.1007/s11222-013-9428-y#Equ23
    # c[m, s, k]: For any dag with m nodes and s outpoints, this is the number of dags which
    # exist with k outpoints for which removing the first layer of outpoints leaves us with that dag.
    c = np.ones((nodes + 1, nodes + 1, nodes + 1), dtype=object)
    c[0, :, :] = 0
    c[:, :, 0] = 0

    for m in range(1, nodes + 1):
        for s in range(1, m + 1):
            for k in range(1, nodes + 1):
                # t is the total ways to link one outpoint to the m nodes on the existing graph
                t = 0
                for i in range(min(m, min_parents), min(m, max_parents) + 1):
                    t += math.comb(m, i)  # The number of ways we can connect our out-point given that it has i parents

                # d is the total dags we could have had where we linked these out-points such that at least one of the s old outpoints are disconnected
                # This is a problem because it would mean that that old out-point is still an out-point,
                # so we remove those from the probabilities.
                d = 0
                for i in range(1, s + 1):
                    # This part is the number of ways we could link these out-points such that less than or equal to i outpoints are disconnected
                    # Explain the inclusion-exclusion principle
                    # Then there are (s-i) "real" outpoints

                    # (2 ** ((m - i) * s - 1)) is how many ways we can link our outpoints to the non-isolated points
                    # math.comb(s, i) is how many ways the i isolated outpoints can be selected from the s total outpoints

                    # ways outpoints can be linked to non-isolated points
                    l = 0
                    for x in range(min(m, min_parents), min(m - i, max_parents) + 1):
                        l += math.comb(m - i, x)

                    sign = (-1) ** (i + 1)

                    if m - i != 0:
                        d += sign * math.comb(s, i) * (l ** k)

                if t ** k < d:
                    print(t ** k, "<", d, f"({m}, {s}, {k}) t={t}")
                c[m, s, k] = t ** k - d

    # a[n, k] is how many graphs there are with n nodes and k out-points, ignoring permutations.
    a = np.ones((nodes + 1, nodes + 1), dtype=object)

    for n in range(1, nodes + 1):
        for k in range(1, n + 1):
            # m is the number of nodes in the hypothetical DAG with the k out-points removed.
            m = n - k

            if m != 0:
                # if that number is zero, then for DP purposes it is still useful to consider that there exists
                # "one" empty graph.

                # Otherwise, we initialise b to 0 as we will be building this recursively.
                a[n, k] = 0

            for s in range(1, m + 1):
                # We add to a[n,k] the number of dags with m nodes and s out-points,
                # multiplied by how many times each appears in a DAG with n nodes and k-outpoints
                a[n, k] += a[m, s] * c[m, s, k]

    a[0, :] = 0
    a[:, 0] = 0

    a_n = np.sum(a[-1], dtype=object)

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
            scaling_factor = c[nodes_remaining][out_points][old_out_points]
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


def generate_random_unconnected_dag_gnp(connectedness: float, nodes: int):
    directed_graph = nx.gnp_random_graph(nodes, connectedness, directed=True)
    directed_acyclic_graph = nx.DiGraph([(u, v) for (u, v) in directed_graph.edges() if u < v])

    return nx.relabel_nodes(directed_acyclic_graph, {node: str(node) for node in list(directed_acyclic_graph.nodes)})


if __name__ == "__main__":
    generate_random_dag(10, 2, 3)
