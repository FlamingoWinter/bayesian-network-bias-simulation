"""
Tests for simulation/build_network/.

The generation pipeline produces random Bayesian networks that model a hiring
scenario.  Two properties matter:

1. Validity — every generated network satisfies the structural contracts that
   the rest of the pipeline depends on (a binary score node, named application
   characteristics, a valid DAG, etc.).

2. Diversity — the algorithm is supposed to sample uniformly from the space of
   all DAGs with the given parameters.  We verify this by checking that the
   distribution of out-point counts at the first layer matches the theoretical
   counts computed by the algorithm's own bookkeeping matrix.
"""

import math
from collections import Counter

import networkx as nx
import numpy as np
import pytest
from scipy.stats import chisquare

from backend.simulation.build_network.generation.generate_categorical_network import (
    generate_random_categorical_network,
)
from backend.simulation.build_network.generation.generate_dag import (
    calculate_out_point_counts,
    generate_random_dag,
)


# ── Structural validity ───────────────────────────────────────────────────────


def test_generated_network_has_a_binary_score_node():
    """Competence must be modelled as hired/not-hired — a two-category node."""
    network = generate_random_categorical_network(nodes=15, seed=1)
    score = network.characteristics[network.score_characteristic]
    assert len(score.category_names) == 2


def test_score_node_is_not_on_the_application_form():
    """Applicants shouldn't self-report their own competence score."""
    network = generate_random_categorical_network(nodes=15, seed=2)
    assert network.score_characteristic not in network.application_characteristics


def test_all_application_nodes_are_in_the_network():
    network = generate_random_categorical_network(nodes=15, seed=3)
    for node in network.application_characteristics:
        assert node in network.characteristics


def test_every_characteristic_has_at_least_two_categories():
    network = generate_random_categorical_network(nodes=15, seed=4)
    for name, c in network.characteristics.items():
        assert len(c.category_names) >= 2, (
            f"'{name}' has only {len(c.category_names)} category"
        )


def test_the_underlying_graph_is_a_directed_acyclic_graph():
    network = generate_random_categorical_network(nodes=15, seed=5)
    graph = network.model.to_directed()
    assert nx.is_directed_acyclic_graph(graph)


def test_network_can_be_sampled_to_produce_an_applicant_population():
    network = generate_random_categorical_network(nodes=15, seed=6)
    applicants = network.sample_applicants(300)
    assert len(applicants.characteristic_instances) == 300


def test_seeded_generation_is_reproducible():
    a = generate_random_categorical_network(nodes=15, seed=99)
    b = generate_random_categorical_network(nodes=15, seed=99)
    assert a.score_characteristic == b.score_characteristic
    assert sorted(a.application_characteristics) == sorted(b.application_characteristics)


# ── Uniform sampling from DAG space ──────────────────────────────────────────
#
# The algorithm samples DAGs by computing a[n, k] — the number of DAGs with n
# nodes and k out-points — and using that to choose layer sizes proportionally.
# We can verify the first-layer distribution empirically against the theoretical
# marginal given by sum_k a[n, k] for each k.


def theoretical_first_layer_distribution(nodes, parents_range):
    """
    Returns a probability vector over possible first-layer out-point counts,
    derived from the same bookkeeping matrix the algorithm uses internally.
    This is the ground truth we compare the sampler against.
    """
    # Reconstruct a[n, k] by running calculate_out_point_counts many times
    # would be circular — instead we replicate the a-matrix construction here.
    min_p, max_p = parents_range
    a = np.ones((nodes + 1, nodes + 1), dtype=object)

    c = np.ones((nodes + 1, nodes + 1, nodes + 1), dtype=object)
    c[0, :, :] = 0
    c[:, :, 0] = 0

    for m in range(1, nodes + 1):
        for s in range(1, m + 1):
            for k in range(1, nodes + 1):
                t = sum(math.comb(m, i) for i in range(min(m, min_p), min(m, max_p) + 1))
                d = 0
                for i in range(1, s + 1):
                    link_ways = sum(
                        math.comb(m - i, x)
                        for x in range(min(m - i, min_p), min(m - i, max_p) + 1)
                    )
                    if m - i != 0:
                        d += ((-1) ** (i + 1)) * math.comb(s, i) * (link_ways ** k)
                c[m, s, k] = t ** k - d

    for n in range(1, nodes + 1):
        for k in range(1, n + 1):
            m = n - k
            if m != 0:
                a[n, k] = 0
            for s in range(1, m + 1):
                a[n, k] += a[m, s] * c[m, s, k]

    a[0, :] = 0
    a[:, 0] = 0

    # Marginal distribution over first-layer out-point count
    counts = np.array([float(a[nodes, k]) for k in range(1, nodes + 1)])
    return counts / counts.sum()


def test_dag_first_layer_out_point_distribution_matches_theoretical():
    """
    The first layer of a generated DAG should have out-point counts distributed
    according to the theoretical distribution encoded in the algorithm's own
    bookkeeping matrix.  A chi-squared test with p > 0.01 confirms this.
    """
    nodes, parents_range = 6, (1, 2)
    n_samples = 400

    observed_counts = Counter()
    for _ in range(n_samples):
        out_point_counts = calculate_out_point_counts(nodes, parents_range)
        observed_counts[out_point_counts[0]] += 1

    theoretical = theoretical_first_layer_distribution(nodes, parents_range)

    # Align observed with all possible first-layer sizes (1..nodes)
    observed = np.array([
        observed_counts.get(k, 0) for k in range(1, nodes + 1)
    ], dtype=float)
    expected = theoretical * n_samples

    # Collapse bins with expected < 5 to avoid chi-squared instability
    mask = expected >= 5
    observed_masked = np.append(observed[mask], observed[~mask].sum())
    expected_masked = np.append(expected[mask], expected[~mask].sum())

    _, p_value = chisquare(observed_masked, expected_masked)
    assert p_value > 0.01, (
        f"DAG first-layer distribution deviates from theoretical (p={p_value:.4f}). "
        "The uniform sampling property may be broken."
    )
