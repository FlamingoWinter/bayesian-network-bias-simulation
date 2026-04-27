"""
Shared pytest fixtures.

Fake / minimal stand-ins are used wherever heavy dependencies (pgmpy,
sklearn, torch) would make tests slow or hard to isolate.  Real objects
are only constructed in integration/ tests.
"""

import os
import sys

# backend/api must be on sys.path so that pytest-django can import
# `test_settings` (which does `from server.settings import *`).
# This must happen before any Django-related import.
_api_dir = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "api")
)
if _api_dir not in sys.path:
    sys.path.insert(0, _api_dir)

from typing import Dict, List, Optional
from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest
from pgmpy.models import BayesianNetwork as pgBN

from backend.api.types import NetworkResponse
from backend.simulation.build_network.bayesian_network import (
    BayesianNetwork,
    Characteristic,
)
from backend.simulation.sample_applicants import Applicants


# ── Minimal BayesianNetwork stub ─────────────────────────────────────────────


class StubBayesianNetwork(BayesianNetwork):
    """Concrete subclass that satisfies the ABC without needing pgmpy inference."""

    def __init__(
        self,
        characteristics: Dict[str, Characteristic],
        score_characteristic: str,
        application_characteristics: List[str],
    ):
        super().__init__(
            model=MagicMock(spec=pgBN),
            characteristics=characteristics,
            score_characteristic=score_characteristic,
            application_characteristics=application_characteristics,
        )

    def to_network_response(self) -> NetworkResponse:
        raise NotImplementedError

    def initialise_characteristics_from_model(self, model):
        return {}

    def sample_conditioned(self):
        raise NotImplementedError

    def sample_applicants(self, count=5000):
        raise NotImplementedError

    def condition_on(self, condition_request):
        raise NotImplementedError


# ── Characteristic helpers ────────────────────────────────────────────────────


def make_characteristic(name: str, categories: List[str]) -> Characteristic:
    c = Characteristic(name, "categorical")
    c.set_categories(categories)
    return c


# ── Applicants fixture ────────────────────────────────────────────────────────

N_APPLICANTS = 200


@pytest.fixture()
def binary_characteristic() -> Characteristic:
    return make_characteristic("gender", ["male", "female"])


@pytest.fixture()
def stub_network(binary_characteristic) -> StubBayesianNetwork:
    score_char = make_characteristic("score", ["0", "1"])
    age_char = make_characteristic("age", ["young", "old"])
    return StubBayesianNetwork(
        characteristics={
            "gender": binary_characteristic,
            "age": age_char,
            "score": score_char,
        },
        score_characteristic="score",
        application_characteristics=["gender", "age"],
    )


@pytest.fixture()
def applicants_df(stub_network) -> pd.DataFrame:
    """A reproducible DataFrame of N_APPLICANTS rows."""
    rng = np.random.default_rng(42)
    n = N_APPLICANTS
    gender = rng.integers(0, 2, size=n)
    age = rng.integers(0, 2, size=n)
    # score is roughly correlated with gender so there is signal
    score = ((gender == 0) & (rng.random(n) > 0.4)).astype(int) | (
        (gender == 1) & (rng.random(n) > 0.7)
    ).astype(int)
    return pd.DataFrame({"gender": gender, "age": age, "score": score})


@pytest.fixture()
def applicants(stub_network, applicants_df) -> Applicants:
    return Applicants(stub_network, applicants_df)


# ── Hand-computed confusion-matrix DataFrame ──────────────────────────────────
#
#  actual    = [1, 1, 1, 1, 0, 0, 0, 0]
#  predicted = [1, 1, 0, 0, 1, 0, 0, 0]
#
#  TP=2  FN=2  FP=1  TN=3
#  hired=3  not_hired=5  competent=4  not_competent=4
#
#  FNR  = FN / competent      = 2/4  = 0.50
#  FPR  = FP / not_competent  = 1/4  = 0.25
#  FDR  = FP / hired          = 1/3
#  FOR  = FN / not_hired      = 2/5  = 0.40
#  acc  = (TP+TN) / total     = 5/8  = 0.625


@pytest.fixture()
def known_confusion_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "actual_score": [1, 1, 1, 1, 0, 0, 0, 0],
            "predicted_score": [1, 1, 0, 0, 1, 0, 0, 0],
            "group": [0, 1, 0, 1, 0, 0, 1, 1],
        }
    )
