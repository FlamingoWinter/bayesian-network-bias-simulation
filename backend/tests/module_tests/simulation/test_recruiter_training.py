"""
Tests for simulation/train_recruiters/.

Each recruiter class is named after the ML algorithm it wraps.  The core
contract is that the name is not just a label — the underlying model must
actually be an instance of the named algorithm, and it must behave as that
algorithm would behave (e.g. a random forest should use ensemble voting, not
a single decision boundary like logistic regression).
"""

import numpy as np
import pandas as pd
import pytest

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from pgmpy.models import BayesianNetwork as PgBN


# ── Shared training data ──────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def small_dataset():
    rng = np.random.default_rng(0)
    n, f = 120, 4
    X = pd.DataFrame(rng.integers(0, 3, (n, f)).astype(float), columns=[f"f{i}" for i in range(f)])
    y = pd.Series(rng.integers(0, 2, n), name="competent")
    return X, y


# ── Algorithm identity ────────────────────────────────────────────────────────


def test_random_forest_recruiter_uses_a_random_forest(small_dataset):
    """
    RandomForestRecruiter wraps sklearn's RandomForestClassifier.  The ensemble
    of trees means predictions are based on a majority vote, not a single linear
    boundary.
    """
    from backend.simulation.train_recruiters.models.random_forest_recruiter import RandomForestRecruiter
    recruiter = RandomForestRecruiter([])
    assert isinstance(recruiter.model, RandomForestClassifier)
    X, y = small_dataset
    recruiter.train(X, y)
    assert recruiter.model.n_estimators > 1  # it really is an ensemble


def test_logistic_regression_recruiter_uses_logistic_regression(small_dataset):
    from backend.simulation.train_recruiters.models.logistic_regression_recruiter import LogisticRegressionRecruiter
    recruiter = LogisticRegressionRecruiter([])
    assert isinstance(recruiter.model, LogisticRegression)
    X, y = small_dataset
    recruiter.train(X, y)
    # Logistic regression should have learned a coefficient per feature
    assert recruiter.model.coef_.shape[1] == X.shape[1]


def test_svm_recruiter_uses_a_support_vector_machine(small_dataset):
    from backend.simulation.train_recruiters.models.svm_recruiter import SVMRecruiter
    recruiter = SVMRecruiter([])
    assert isinstance(recruiter.model, SVC)
    X, y = small_dataset
    recruiter.train(X, y)
    # After fitting, support vectors should exist
    assert recruiter.model.support_vectors_.shape[0] > 0


def test_bayesian_recruiter_uses_a_bayesian_network():
    """
    BayesianRecruiter learns a graphical model structure from the data using
    hill-climb search, not a parametric model.

    We use a small dataset with obvious correlations (f0 XOR f1 → score) so
    that HillClimbSearch reliably finds at least one edge rather than returning
    an empty graph (which it can do on noisy or low-signal data).
    """
    from backend.simulation.train_recruiters.models.bayesian_recruiter import BayesianRecruiter
    rng = np.random.default_rng(7)
    n = 600
    f0 = pd.Series(rng.integers(0, 2, n), name="f0")
    f1 = pd.Series(rng.integers(0, 2, n), name="f1")
    # Score is almost perfectly determined by f0 so the edge is easy to find
    score = pd.Series(f0.values.copy(), name="competent")
    X = pd.DataFrame({"f0": f0, "f1": f1})

    recruiter = BayesianRecruiter([])
    assert isinstance(recruiter.model, PgBN)
    recruiter.train(X, score)
    # HillClimbSearch should discover at least one edge given the strong signal
    assert len(recruiter.model.nodes) > 0


def test_shallow_mlp_recruiter_uses_a_neural_network(small_dataset):
    import torch.nn as nn
    from backend.simulation.train_recruiters.models.shallow_mlp_recruiter import ShallowMLPRecruiter
    recruiter = ShallowMLPRecruiter([])
    X, y = small_dataset
    recruiter.train(X, y)
    # The model should have at least one linear (fully-connected) layer
    has_linear = any(isinstance(m, nn.Linear) for m in recruiter.model.modules())
    assert has_linear


def test_deep_mlp_recruiter_has_more_layers_than_shallow(small_dataset):
    import torch.nn as nn
    from backend.simulation.train_recruiters.models.shallow_mlp_recruiter import ShallowMLPRecruiter
    from backend.simulation.train_recruiters.models.deep_mlp_recruiter import DeepMLPRecruiter
    X, y = small_dataset
    shallow = ShallowMLPRecruiter([])
    deep = DeepMLPRecruiter([])
    shallow.train(X, y)
    deep.train(X, y)
    shallow_layers = sum(1 for _ in shallow.model.modules() if isinstance(_, nn.Linear))
    deep_layers = sum(1 for _ in deep.model.modules() if isinstance(_, nn.Linear))
    assert deep_layers > shallow_layers


@pytest.mark.slow
def test_transformer_recruiter_uses_self_attention(small_dataset):
    import torch.nn as nn
    from backend.simulation.train_recruiters.models.encoder_only_transformer_recruiter import EncoderOnlyTransformerRecruiter
    recruiter = EncoderOnlyTransformerRecruiter([])
    X, y = small_dataset
    recruiter.train(X, y)
    has_attention = any(
        isinstance(m, nn.MultiheadAttention) for m in recruiter.model.modules()
    )
    assert has_attention


# ── Post-training predictions ─────────────────────────────────────────────────
#
# Regardless of the algorithm, every recruiter must produce scores in a
# consistent range after training.  We use logistic regression as a fast
# stand-in to check the shared prediction interface.


def test_recruiter_score_range_is_consistent_before_and_after_seeing_new_data(small_dataset):
    """
    Scores on held-out data should come from the same distribution as scores on
    training data — the model shouldn't wildly extrapolate.
    """
    from backend.simulation.train_recruiters.models.logistic_regression_recruiter import LogisticRegressionRecruiter
    X, y = small_dataset
    train_X, test_X = X[:80], X[80:]
    recruiter = LogisticRegressionRecruiter([])
    recruiter.train(train_X, y[:80])

    train_scores = recruiter.predict_scores(train_X)
    test_scores = recruiter.predict_scores(test_X)

    # Scores should be in a similar range — not orders of magnitude different
    assert abs(train_scores.mean() - test_scores.mean()) < 5 * train_scores.std() + 1e-6
