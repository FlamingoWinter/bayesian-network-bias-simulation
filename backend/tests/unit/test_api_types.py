"""
Unit tests for backend/api/schemas.py.

Covers Pydantic validation, blank-sentinel stripping, and default fallbacks
for both SimulateRequest and NetworkRequest.
"""

import pytest
from pydantic import ValidationError

from backend.api.schemas import (
    NetworkRequest,
    PredefinedNetworkRequest,
    SimulateRequest,
    new_random_network_request,
    new_simulate_request,
)


# ── SimulateRequest ───────────────────────────────────────────────────────────


class TestSimulateRequest:
    def test_defaults(self):
        req = SimulateRequest()
        assert req.candidates_to_generate == 10_000
        assert req.train_proportion == 0.9
        assert req.recruiters == {"random_forest": ["no_mitigation"]}
        assert req.protected_characteristic == ""
        assert req.score_threshold == 0

    def test_accepts_valid_values(self):
        req = SimulateRequest(
            candidates_to_generate=500,
            train_proportion=0.8,
            recruiters={"logistic_regression": ["demographic_parity"]},
            protected_characteristic="gender",
            score_threshold=0.5,
        )
        assert req.candidates_to_generate == 500
        assert req.protected_characteristic == "gender"

    def test_blank_string_falls_back_to_default(self):
        req = SimulateRequest.model_validate({"protected_characteristic": ""})
        assert req.protected_characteristic == ""

    def test_empty_list_stripped(self):
        req = SimulateRequest.model_validate({"recruiters": []})
        assert req.recruiters == {"random_forest": ["no_mitigation"]}

    def test_list_with_blank_string_stripped(self):
        req = SimulateRequest.model_validate({"recruiters": [""]})
        assert req.recruiters == {"random_forest": ["no_mitigation"]}

    def test_new_simulate_request_factory(self):
        req = new_simulate_request(candidates_to_generate=200)
        assert req.candidates_to_generate == 200
        assert req.train_proportion == 0.9  # default preserved


# ── NetworkRequest ────────────────────────────────────────────────────────────


class TestNetworkRequest:
    def test_defaults(self):
        req = NetworkRequest()
        assert req.random_or_predefined == "random"
        assert req.number_of_nodes == 12
        assert req.parents_range == (1, 3)
        assert req.mutual_information_range == (0.1, 0.9)

    def test_accepts_valid_values(self):
        req = NetworkRequest(number_of_nodes=20, parents_range=(2, 4))
        assert req.number_of_nodes == 20
        assert req.parents_range == (2, 4)

    def test_empty_string_key_stripped(self):
        req = NetworkRequest.model_validate({"number_of_nodes": ""})
        assert req.number_of_nodes == 12

    def test_empty_list_stripped(self):
        req = NetworkRequest.model_validate({"parents_range": []})
        assert req.parents_range == (1, 3)

    def test_partial_blank_in_tuple_uses_default_for_blank_element(self):
        # Frontend may send ["", 4] when only the upper bound is set
        req = NetworkRequest.model_validate({"parents_range": ["", 4]})
        assert req.parents_range == (1, 4)

    def test_new_random_network_request_strips_predefined_model(self):
        req = new_random_network_request(
            number_of_nodes=8, predefined_model="sprinkler"
        )
        assert req.number_of_nodes == 8
        assert not hasattr(req, "predefined_model")

    def test_values_per_variable_is_dict(self):
        req = NetworkRequest()
        assert isinstance(req.values_per_variable, dict)
        assert all(isinstance(k, str) for k in req.values_per_variable)


# ── PredefinedNetworkRequest ──────────────────────────────────────────────────


class TestPredefinedNetworkRequest:
    def test_requires_predefined_literal(self):
        req = PredefinedNetworkRequest(
            random_or_predefined="predefined", predefined_model="sprinkler"
        )
        assert req.predefined_model == "sprinkler"

    def test_wrong_literal_raises(self):
        with pytest.raises(ValidationError):
            PredefinedNetworkRequest(  # type: ignore
                random_or_predefined="random", predefined_model="sprinkler"
            )
