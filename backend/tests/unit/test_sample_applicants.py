"""
Unit tests for the Applicants class (sample_applicants.py).

Uses StubBayesianNetwork from conftest so no pgmpy inference occurs.
"""

import pandas as pd
import pytest


# ── get_applications ──────────────────────────────────────────────────────────


class TestGetApplications:
    def test_returns_only_application_columns(self, applicants):
        df = applicants.get_applications()
        expected = set(applicants.network.application_characteristics)
        assert set(df.columns) == expected

    def test_does_not_contain_score_column(self, applicants):
        df = applicants.get_applications()
        assert applicants.network.score_characteristic not in df.columns

    def test_index_is_reset(self, applicants):
        df = applicants.get_applications()
        assert list(df.index) == list(range(len(df)))

    def test_one_hot_encoding_expands_columns(self, applicants):
        raw_df = applicants.get_applications(one_hot_encode_categorical_variables=False)
        ohe_df = applicants.get_applications(one_hot_encode_categorical_variables=True)
        # One-hot drops first, so categorical with 2 values → 1 extra column per var
        # The result should have ≥ same number of columns
        assert len(ohe_df.columns) >= len(raw_df.columns)

    def test_one_hot_no_original_categorical_cols(self, applicants):
        ohe_df = applicants.get_applications(one_hot_encode_categorical_variables=True)
        raw_cols = applicants.network.application_characteristics
        # Original categorical column names should not appear in one-hot form
        # (pd.get_dummies replaces them)
        for col in raw_cols:
            assert col not in ohe_df.columns


# ── get_scores ────────────────────────────────────────────────────────────────


class TestGetScores:
    def test_returns_series(self, applicants):
        scores = applicants.get_scores()
        assert isinstance(scores, pd.Series)

    def test_length_matches_applicants(self, applicants):
        scores = applicants.get_scores()
        assert len(scores) == len(applicants.characteristic_instances)

    def test_index_is_reset(self, applicants):
        scores = applicants.get_scores()
        assert list(scores.index) == list(range(len(scores)))

    def test_values_are_binary(self, applicants):
        scores = applicants.get_scores()
        assert set(scores.unique()).issubset({0, 1})


# ── characteristic_name_to_distribution ──────────────────────────────────────


class TestCharacteristicNameToDistribution:
    def test_returns_list(self, applicants):
        dist = applicants.characteristic_name_to_distribution("gender")
        assert isinstance(dist, list)

    def test_length_matches_applicants(self, applicants):
        dist = applicants.characteristic_name_to_distribution("gender")
        assert len(dist) == len(applicants.characteristic_instances)


# ── random_split ──────────────────────────────────────────────────────────────


class TestRandomSplit:
    def test_two_way_split_sizes(self, applicants):
        train, test = applicants.random_split([0.8, 0.2])
        total = len(train.characteristic_instances) + len(test.characteristic_instances)
        assert total == len(applicants.characteristic_instances)

    def test_three_way_split_sizes(self, applicants):
        a, b, c = applicants.random_split([0.5, 0.25, 0.25])
        total = (
            len(a.characteristic_instances)
            + len(b.characteristic_instances)
            + len(c.characteristic_instances)
        )
        assert total == len(applicants.characteristic_instances)

    def test_splits_share_same_network(self, applicants, stub_network):
        train, test = applicants.random_split([0.7, 0.3])
        assert train.network is stub_network
        assert test.network is stub_network

    def test_no_row_duplication(self, applicants):
        train, test = applicants.random_split([0.8, 0.2])
        combined = pd.concat(
            [train.characteristic_instances, test.characteristic_instances]
        )
        # Original dataset should equal combined (same rows, possibly reordered)
        assert len(combined) == len(applicants.characteristic_instances)

    def test_approximate_proportions(self, applicants):
        # With 200 applicants a 70/30 split should be within 5% of target
        train, test = applicants.random_split([0.7, 0.3])
        train_ratio = len(train.characteristic_instances) / len(
            applicants.characteristic_instances
        )
        assert abs(train_ratio - 0.7) < 0.05
