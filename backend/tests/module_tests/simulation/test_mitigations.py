"""
Tests for simulation/train_recruiters/mitigation/.

A mitigation adjusts the hiring threshold independently per group to make
outcomes fairer.  The contract for each mitigation is either:

  (a) Successful — it achieves the stated fairness goal on the training data it
      was calibrated on (e.g. demographic parity makes hiring rates equal).

  (b) Locally optimal — for optimisation-based mitigations that use simulated
      annealing, the solution may not be globally optimal, but it should be at
      a local minimum: small perturbations to the hiring proportions should not
      reduce the loss.
"""

import numpy as np
import pandas as pd
import pytest


# ── Shared dataset ────────────────────────────────────────────────────────────
#
# Group 0 has higher raw scores than group 1, creating a measurable disparity
# in hiring outcomes before any mitigation is applied.


def make_biased_dataset(seed=0):
    rng = np.random.default_rng(seed)
    n = 300

    group = pd.Series(np.repeat([0, 1], n // 2), name="group")
    # Group 0 tends to score higher
    raw_scores = pd.Series(
        np.where(group == 0, rng.uniform(0.5, 1.0, n), rng.uniform(0.0, 0.6, n)),
        name="score",
    )
    competence = pd.Series((raw_scores > 0.5).astype(int), name="competent")

    return raw_scores, competence, group


def initialise(mitigation, scores, competence, group):
    """Calibrate a mitigation using the provided data as both train and holdout."""
    mitigation.extract_hiring_proportions_from_training_and_holdout(
        competence, group, competence, scores, group
    )
    return mitigation


# ── Demographic parity ────────────────────────────────────────────────────────


def test_demographic_parity_produces_equal_hiring_rates_across_groups():
    """
    After applying demographic parity, both groups should be hired at the same
    overall rate, regardless of their underlying score distribution.
    """
    from backend.simulation.train_recruiters.mitigation.demographic_parity import (
        SatisfyDemographicParity,
    )

    scores, competence, group = make_biased_dataset()
    mitigation = initialise(SatisfyDemographicParity(), scores, competence, group)
    decisions = mitigation.convert_scores_to_decisions(scores, group)

    rate_0 = decisions[group == 0].mean()
    rate_1 = decisions[group == 1].mean()
    assert abs(rate_0 - rate_1) < 0.05, (
        f"Hiring rates differ by {abs(rate_0 - rate_1):.2f} after demographic parity"
    )


# ── Proportional parity ───────────────────────────────────────────────────────


def test_proportional_parity_hires_each_group_at_its_own_competence_rate():
    """
    Proportional parity sets each group's hiring rate to match its competence
    rate, so that a randomly selected hire is no more likely to be incompetent
    in one group than another.
    """
    from backend.simulation.train_recruiters.mitigation.proportional_parity import (
        SatisfyProportionalParity,
    )

    scores, competence, group = make_biased_dataset()
    mitigation = initialise(SatisfyProportionalParity(), scores, competence, group)
    decisions = mitigation.convert_scores_to_decisions(scores, group)

    for g in [0, 1]:
        mask = group == g
        competence_rate = competence[mask].mean()
        hiring_rate = decisions[mask].mean()
        assert abs(hiring_rate - competence_rate) < 0.08, (
            f"Group {g}: hiring rate {hiring_rate:.2f} deviates too much from "
            f"competence rate {competence_rate:.2f}"
        )


# ── Optimisation-based mitigations: local optimum property ───────────────────
#
# These mitigations use simulated annealing to find hiring proportions that
# minimise a loss function.  We can't demand a global optimum, but we can
# check that the found solution is at least locally stable: perturbing each
# group's proportion by ±2% should not decrease the loss.


def assert_locally_optimal(mitigation, scores, competence, group, tolerance=0.02):
    """
    Verify that no small perturbation of the stored proportions improves the loss.
    """
    props = mitigation.proportion_hireds.copy()
    baseline = mitigation.loss(props, competence, scores, group)

    for i in range(len(props)):
        for delta in [+0.02, -0.02]:
            perturbed = props.copy()
            perturbed[i] = np.clip(perturbed[i] + delta, 0.01, 0.99)
            perturbed_loss = mitigation.loss(perturbed, competence, scores, group)
            assert perturbed_loss >= baseline - tolerance, (
                f"Perturbing proportion[{i}] by {delta:+.2f} reduces loss from "
                f"{baseline:.4f} to {perturbed_loss:.4f} — not a local optimum"
            )


@pytest.mark.slow
def test_fnr_equality_mitigation_reaches_a_local_optimum():
    """
    The mitigation minimises the variance in false-negative rates across groups.
    After calibration, nudging any group's hiring proportion should not reduce
    that variance.
    """
    from backend.simulation.train_recruiters.mitigation.equalised_odds.optimise_for_fnr_equality import (
        OptimiseForFNREquality,
    )

    scores, competence, group = make_biased_dataset(seed=1)
    mitigation = initialise(OptimiseForFNREquality(), scores, competence, group)
    assert_locally_optimal(mitigation, scores, competence, group)


@pytest.mark.slow
def test_fpr_equality_mitigation_reaches_a_local_optimum():
    from backend.simulation.train_recruiters.mitigation.equalised_odds.optimise_for_fpr_equality import (
        OptimiseForFPREquality,
    )

    scores, competence, group = make_biased_dataset(seed=2)
    mitigation = initialise(OptimiseForFPREquality(), scores, competence, group)
    assert_locally_optimal(mitigation, scores, competence, group)


@pytest.mark.slow
def test_fnr_and_fpr_equality_mitigation_reaches_a_local_optimum():
    from backend.simulation.train_recruiters.mitigation.equalised_odds.optimise_for_fnr_and_fpr_equality import (
        OptimiseForFNRAndFPREquality,
    )

    scores, competence, group = make_biased_dataset(seed=3)
    mitigation = initialise(OptimiseForFNRAndFPREquality(), scores, competence, group)
    assert_locally_optimal(mitigation, scores, competence, group)


@pytest.mark.slow
def test_fdr_equality_mitigation_reaches_a_local_optimum():
    from backend.simulation.train_recruiters.mitigation.predictive_parity.optimise_for_fdr_equality import (
        OptimiseForFDREquality,
    )

    scores, competence, group = make_biased_dataset(seed=4)
    mitigation = initialise(OptimiseForFDREquality(), scores, competence, group)
    assert_locally_optimal(mitigation, scores, competence, group)


@pytest.mark.slow
def test_for_equality_mitigation_reaches_a_local_optimum():
    from backend.simulation.train_recruiters.mitigation.predictive_parity.optimise_for_for_equality import (
        OptimiseForFOREquality,
    )

    scores, competence, group = make_biased_dataset(seed=5)
    mitigation = initialise(OptimiseForFOREquality(), scores, competence, group)
    assert_locally_optimal(mitigation, scores, competence, group)
