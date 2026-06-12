"""
Unit tests for the network-building layer.

generate_dag tests focus on graph-structural properties rather than exact
topology (which is random), so they are determinism-agnostic.

choose_characteristics tests verify the documented selection rules for each
condition without requiring a full Bayesian Network.
"""

import networkx as nx
import pytest

from backend.simulation.build_network.characteristic import Characteristic
from backend.simulation.build_network.generation.choose_characteristics import (
    choose_application,
    choose_protected,
    choose_score,
)
from backend.simulation.build_network.generation.generate_dag import (
    generate_random_dag,
    sample_bounded_binomial,
)


# ── generate_random_dag structural properties ─────────────────────────────────


class TestGenerateRandomDag:
    @pytest.fixture(scope="class")
    def dag(self):
        """Single shared DAG — generation is slow."""
        return generate_random_dag(10, (1, 3))

    def test_returns_digraph(self, dag):
        assert isinstance(dag, nx.DiGraph)

    def test_node_count_is_correct(self, dag):
        assert len(dag.nodes) == 10

    def test_is_acyclic(self, dag):
        assert nx.is_directed_acyclic_graph(dag)

    def test_nodes_are_strings(self, dag):
        assert all(isinstance(n, str) for n in dag.nodes)

    def test_has_at_least_one_root(self, dag):
        roots = [n for n, d in dag.in_degree() if d == 0]
        assert len(roots) >= 1

    def test_has_at_least_one_leaf(self, dag):
        leaves = [n for n, d in dag.out_degree() if d == 0]
        assert len(leaves) >= 1

    @pytest.mark.parametrize("nodes,parents_range", [(5, (1, 2)), (8, (1, 3))])
    def test_various_sizes(self, nodes, parents_range):
        dag = generate_random_dag(nodes, parents_range)
        assert len(dag.nodes) == nodes
        assert nx.is_directed_acyclic_graph(dag)


# ── sample_bounded_binomial ───────────────────────────────────────────────────


class TestSampleBoundedBinomial:
    def test_result_within_bounds(self):
        for _ in range(50):
            result = sample_bounded_binomial(10, 0.5, (2, 5))
            assert 2 <= result <= 5

    def test_n_smaller_than_lower_bound_returns_n(self):
        result = sample_bounded_binomial(1, 0.5, (3, 6))
        assert result == 1


# ── choose_score ──────────────────────────────────────────────────────────────
#
# Score must NOT be a root, direct child of a root, or grandchild of a root.


class TestChooseScore:
    @pytest.fixture()
    def simple_dag(self):
        #  0 → 1 → 3 → 5
        #  0 → 2 → 4 → 5
        g = nx.DiGraph()
        g.add_edges_from([(0, 1), (1, 3), (3, 5), (0, 2), (2, 4), (4, 5)])
        return nx.relabel_nodes(g, str)

    def test_score_is_not_root(self, simple_dag):
        roots = {n for n, d in simple_dag.in_degree() if d == 0}
        score = choose_score(simple_dag)
        assert score not in roots

    def test_score_not_direct_child_of_root(self, simple_dag):
        roots = {n for n, d in simple_dag.in_degree() if d == 0}
        direct_children = {c for r in roots for c in simple_dag.successors(r)}
        score = choose_score(simple_dag)
        assert score not in direct_children

    def test_score_is_a_valid_node(self, simple_dag):
        score = choose_score(simple_dag)
        assert score in simple_dag.nodes

    def test_raises_when_no_candidates(self):
        # A three-node chain: 0→1→2 — every non-root is too close to the root
        g = nx.DiGraph()
        g.add_edges_from([("0", "1"), ("1", "2")])
        with pytest.raises(Exception, match="choose_score failed"):
            choose_score(g)


# ── choose_protected ──────────────────────────────────────────────────────────


class TestChooseProtected:
    def test_protected_is_root(self):
        g = nx.DiGraph()
        g.add_edges_from([("a", "b"), ("b", "c"), ("d", "e")])
        roots = {n for n, deg in g.in_degree() if deg == 0}
        protected = choose_protected(g)
        assert protected in roots


# ── choose_application ────────────────────────────────────────────────────────
#
# Four conditions, each with documented inclusion/exclusion rules.


@pytest.fixture()
def medium_dag():
    """12-node DAG with known structure for choose_application tests."""
    g = nx.DiGraph()
    # root nodes: 0, 1
    # score deep inside: 10
    g.add_edges_from(
        [
            ("0", "2"),
            ("0", "3"),
            ("1", "4"),
            ("1", "5"),
            ("2", "6"),
            ("3", "7"),
            ("4", "8"),
            ("5", "9"),
            ("6", "10"),
            ("7", "10"),
            ("8", "11"),
            ("9", "11"),
        ]
    )
    return g


class TestChooseApplication:
    score = "10"
    protected = "0"

    def test_condition1_excludes_score_and_protected(self, medium_dag):
        result = choose_application(medium_dag, 1, self.score, self.protected, 5)
        assert self.score not in result
        assert self.protected not in result
        assert len(result) == 5

    def test_condition2_includes_protected(self, medium_dag):
        result = choose_application(medium_dag, 2, self.score, self.protected, 5)
        assert self.protected in result
        assert self.score not in result
        assert len(result) == 5

    def test_condition3_returns_correct_size(self, medium_dag):
        # medium_dag has 2 proxy neighbours of "0", so application_size must
        # be a multiple of 2 and ≤ 2*2=4 for condition 3 (which takes half
        # from proxies and half from the remaining pool).
        result = choose_application(medium_dag, 3, self.score, self.protected, 4)
        assert len(result) == 4
        assert self.score not in result

    def test_condition4_excludes_two_hop_neighbours(self, medium_dag):
        result = choose_application(medium_dag, 4, self.score, self.protected, 3)
        two_hop = {"0", "2", "3", "6", "7"}  # protected + its 1-hop + their 1-hop
        for node in result:
            assert node not in two_hop

    def test_unknown_condition_raises(self, medium_dag):
        with pytest.raises(ValueError, match="Unknown condition"):
            choose_application(medium_dag, 99, self.score, self.protected)


# ── Characteristic ────────────────────────────────────────────────────────────


class TestCharacteristic:
    def test_set_categories_changes_type(self):
        c = Characteristic("age", "categorical")
        c.set_categories(["young", "old"])
        assert c.type == "categorical"
        assert c.category_names == ["young", "old"]

    def test_to_characteristic_response(self):
        from backend.api.schemas import CharacteristicResponse

        c = Characteristic("race", "categorical")
        c.set_categories(["A", "B"])
        resp = c.to_characteristic_response([0.6, 0.4])
        assert isinstance(resp, CharacteristicResponse)
        assert resp.name == "race"
        assert resp.categoryNames == ["A", "B"]
        assert resp.priorDistribution == [0.6, 0.4]

    def test_to_characteristic_response_no_prior(self):
        c = Characteristic("x", "categorical")
        c.set_categories(["0", "1"])
        resp = c.to_characteristic_response()
        assert resp.priorDistribution is None
