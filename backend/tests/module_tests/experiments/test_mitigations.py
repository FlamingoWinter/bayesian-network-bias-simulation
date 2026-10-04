"""
Tests for experiments/mitigations.py.

This experiment benchmarks every bias mitigation strategy against a random
forest recruiter on a large random network.  The tests verify that the pipeline
calls its stages in the correct order and with the right configuration —
without actually running the slow experiment (which requires a database and
takes many minutes).
"""

from datetime import datetime
from unittest.mock import MagicMock, patch, call


def run_with_mocks():
    """
    Run mitigations_run() with all external dependencies mocked out.
    Returns the mock objects so tests can inspect what was called.
    """
    mock_network = MagicMock()
    mock_network.model.to_directed.return_value = MagicMock()
    mock_network.characteristics = {"protected": MagicMock()}
    mock_applicants = MagicMock()
    mock_engine = MagicMock()
    mock_recruiter_analysis = MagicMock()

    with (
        patch("backend.experiments.mitigations.setup_experiment") as mock_setup,
        patch("backend.experiments.mitigations.choose_application") as mock_choose,
        patch("backend.experiments.mitigations.simulate") as mock_simulate,
        patch("backend.experiments.mitigations.save_run_to_db") as mock_save_run,
        patch("backend.experiments.mitigations.save_recruiter_run_to_db") as mock_save_recruiter,
    ):
        mock_setup.return_value = (
            datetime.now(), mock_engine, mock_network, mock_applicants, "score", "protected"
        )
        mock_simulate.return_value = {MagicMock(): mock_recruiter_analysis}
        mock_save_run.return_value = 42

        from backend.experiments.mitigations import mitigations_run
        mitigations_run()

        return {
            "setup": mock_setup,
            "choose_application": mock_choose,
            "simulate": mock_simulate,
            "save_run": mock_save_run,
            "save_recruiter": mock_save_recruiter,
        }


def test_experiment_starts_by_setting_up_network_and_applicants():
    """setup_experiment() must be called before any simulation runs."""
    mocks = run_with_mocks()
    mocks["setup"].assert_called_once()


def test_experiment_uses_condition_1_application_form():
    """
    The mitigations experiment always uses condition 1 — a random set of
    application features that excludes the protected characteristic.
    """
    mocks = run_with_mocks()
    args = mocks["choose_application"].call_args
    condition_arg = args.args[1]  # second positional argument is the condition
    assert condition_arg == 1


def test_experiment_runs_a_random_forest_with_all_mitigation_strategies():
    """
    The point of the experiment is to compare every mitigation strategy.
    A random forest recruiter with all 11 mitigations should be passed to simulate().
    """
    from backend.simulation.train_recruiters.models.random_forest_recruiter import RandomForestRecruiter

    mocks = run_with_mocks()
    recruiters = mocks["simulate"].call_args.args[1]

    assert len(recruiters) == 1
    assert isinstance(recruiters[0], RandomForestRecruiter)
    assert len(recruiters[0].mitigations) == 11


def test_experiment_saves_results_to_the_database():
    """Results must be persisted — otherwise the experiment produces nothing."""
    mocks = run_with_mocks()
    mocks["save_run"].assert_called_once()
    mocks["save_recruiter"].assert_called_once()


def test_experiment_pipeline_order_is_setup_then_simulate_then_save():
    """
    The pipeline must execute in order: setup → choose application →
    simulate → save.  Out-of-order execution would produce incorrect results
    (e.g. saving before simulating).
    """
    from unittest.mock import call as C

    call_order = []

    mock_network = MagicMock()
    mock_network.model.to_directed.return_value = MagicMock()
    mock_network.characteristics = {"protected": MagicMock()}

    with (
        patch("backend.experiments.mitigations.setup_experiment",
              side_effect=lambda: call_order.append("setup") or
              (datetime.now(), MagicMock(), mock_network, MagicMock(), "score", "protected")) as _,
        patch("backend.experiments.mitigations.choose_application",
              side_effect=lambda *a, **k: call_order.append("choose")) as _,
        patch("backend.experiments.mitigations.simulate",
              side_effect=lambda *a, **k: call_order.append("simulate") or {MagicMock(): MagicMock()}) as _,
        patch("backend.experiments.mitigations.save_run_to_db",
              side_effect=lambda *a, **k: call_order.append("save_run") or 1) as _,
        patch("backend.experiments.mitigations.save_recruiter_run_to_db",
              side_effect=lambda *a, **k: call_order.append("save_recruiter")) as _,
    ):
        from backend.experiments.mitigations import mitigations_run
        mitigations_run()

    assert call_order.index("setup") < call_order.index("choose")
    assert call_order.index("choose") < call_order.index("simulate")
    assert call_order.index("simulate") < call_order.index("save_run")
    assert call_order.index("save_run") < call_order.index("save_recruiter")
