"""
Tests for experiments/network_structure_conditions.py.

This experiment measures how the structure of the job application form affects
recruiter bias.  It runs the same network four times, each time constructing a
different application form:

  Condition 1 — random features, no protected characteristic
  Condition 2 — random features, protected characteristic included
  Condition 3 — proxy features (neighbours of the protected characteristic)
  Condition 4 — features at least 2 hops away from the protected characteristic

The tests verify that all four conditions are tested with all recruiter types,
and that results are saved once per condition.
"""

from datetime import datetime
from unittest.mock import MagicMock, patch


def run_with_mocks():
    mock_network = MagicMock()
    mock_network.model.to_directed.return_value = MagicMock()
    mock_network.characteristics = {"protected": MagicMock()}
    mock_applicants = MagicMock()
    mock_engine = MagicMock()

    simulate_calls = []
    choose_calls = []
    save_run_calls = []
    save_recruiter_calls = []

    def fake_simulate(applicants, recruiters, *args, **kwargs):
        simulate_calls.append(recruiters)
        # Return one entry per recruiter type so save_recruiter_run_to_db is
        # called once per recruiter per condition (7 types × 4 conditions = 28).
        return {MagicMock(): MagicMock() for _ in range(7)}

    def fake_choose(graph, condition, *args, **kwargs):
        choose_calls.append(condition)
        return []

    def fake_save_run(*args, **kwargs):
        save_run_calls.append(args)
        return len(save_run_calls)

    def fake_save_recruiter(*args, **kwargs):
        save_recruiter_calls.append(args)

    with (
        patch("backend.experiments.network_structure_conditions.setup_experiment",
              return_value=(datetime.now(), mock_engine, mock_network, mock_applicants, "score", "protected")),
        patch("backend.experiments.network_structure_conditions.choose_application", side_effect=fake_choose),
        patch("backend.experiments.network_structure_conditions.simulate", side_effect=fake_simulate),
        patch("backend.experiments.network_structure_conditions.save_run_to_db", side_effect=fake_save_run),
        patch("backend.experiments.network_structure_conditions.save_recruiter_run_to_db", side_effect=fake_save_recruiter),
    ):
        from backend.experiments.network_structure_conditions import network_structure_conditions_run
        network_structure_conditions_run()

    return {
        "simulate_calls": simulate_calls,
        "choose_calls": choose_calls,
        "save_run_calls": save_run_calls,
        "save_recruiter_calls": save_recruiter_calls,
    }


def test_experiment_tests_all_four_application_form_conditions():
    """
    The experiment must run all four conditions.  Skipping one would make the
    results for that structural assumption missing from the database.
    """
    results = run_with_mocks()
    assert sorted(results["choose_calls"]) == [1, 2, 3, 4]


def test_experiment_runs_simulation_once_per_condition():
    results = run_with_mocks()
    assert len(results["simulate_calls"]) == 4


def test_experiment_tests_all_recruiter_types_for_each_condition():
    """
    Each condition should be evaluated against every recruiter type so that the
    results are comparable across both dimensions (structure and algorithm).
    """
    from backend.simulation.train_recruiters.models.random_forest_recruiter import RandomForestRecruiter
    from backend.simulation.train_recruiters.models.logistic_regression_recruiter import LogisticRegressionRecruiter
    from backend.simulation.train_recruiters.models.svm_recruiter import SVMRecruiter
    from backend.simulation.train_recruiters.models.bayesian_recruiter import BayesianRecruiter
    from backend.simulation.train_recruiters.models.shallow_mlp_recruiter import ShallowMLPRecruiter
    from backend.simulation.train_recruiters.models.deep_mlp_recruiter import DeepMLPRecruiter
    from backend.simulation.train_recruiters.models.encoder_only_transformer_recruiter import EncoderOnlyTransformerRecruiter

    expected_types = {
        RandomForestRecruiter, LogisticRegressionRecruiter, SVMRecruiter,
        BayesianRecruiter, ShallowMLPRecruiter, DeepMLPRecruiter,
        EncoderOnlyTransformerRecruiter,
    }

    results = run_with_mocks()
    for recruiters in results["simulate_calls"]:
        actual_types = {type(r) for r in recruiters}
        assert actual_types == expected_types


def test_experiment_saves_one_result_per_condition():
    """
    Each condition's results must be persisted separately so they can be
    compared against each other in analysis.
    """
    results = run_with_mocks()
    assert len(results["save_run_calls"]) == 4


def test_experiment_saves_one_recruiter_result_per_recruiter_per_condition():
    """
    With 7 recruiter types and 4 conditions, 28 recruiter-level rows should
    be written to the database.
    """
    results = run_with_mocks()
    assert len(results["save_recruiter_calls"]) == 28
