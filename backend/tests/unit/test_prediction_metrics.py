"""
Unit tests for GroupPredictionInformation (prediction_metrics.py).

Uses a hand-computed confusion matrix so every assertion can be
verified without running any ML model:

    actual    = [1, 1, 1, 1, 0, 0, 0, 0]
    predicted = [1, 1, 0, 0, 1, 0, 0, 0]

    TP = 2  FN = 2  FP = 1  TN = 3

    hired         = TP + FP = 3
    not_hired     = FN + TN = 5
    competent     = TP + FN = 4
    not_competent = FP + TN = 4

    FNR = FN / competent      = 2/4 = 0.50
    FPR = FP / not_competent  = 1/4 = 0.25
    FDR = FP / hired          = 1/3
    FOR = FN / not_hired      = 2/5 = 0.40
    acc = (TP + TN) / total   = 5/8 = 0.625
"""

import pytest

from backend.simulation.measure_bias.prediction_metrics import (
    GroupPredictionInformation,
    confusion_matrix,
)


@pytest.fixture()
def df(known_confusion_df):
    return known_confusion_df


# ── confusion_matrix helper ───────────────────────────────────────────────────


class TestConfusionMatrix:
    def test_returns_tp_fp_tn_fn(self, df):
        tp, fp, tn, fn = confusion_matrix(df)
        assert tp == 2
        assert fp == 1
        assert tn == 3
        assert fn == 2

    def test_all_correct(self):
        import pandas as pd

        perfect = pd.DataFrame(
            {"actual_score": [1, 0, 1, 0], "predicted_score": [1, 0, 1, 0]}
        )
        tp, fp, tn, fn = confusion_matrix(perfect)
        assert tp == 2
        assert fp == 0
        assert tn == 2
        assert fn == 0

    def test_all_wrong(self):
        import pandas as pd

        inverted = pd.DataFrame(
            {"actual_score": [1, 0, 1, 0], "predicted_score": [0, 1, 0, 1]}
        )
        tp, fp, tn, fn = confusion_matrix(inverted)
        assert tp == 0
        assert fp == 2
        assert tn == 0
        assert fn == 2


# ── GroupPredictionInformation counts ────────────────────────────────────────


class TestGroupPredictionInformationCounts:
    @pytest.fixture(autouse=True)
    def setup(self, df):
        self.info = GroupPredictionInformation(df)

    def test_total(self):
        assert self.info.total == 8

    def test_hired_and_competent(self):
        assert self.info.hired_and_competent == 2  # TP

    def test_hired_but_not_competent(self):
        assert self.info.hired_but_not_competent == 1  # FP

    def test_not_hired_and_not_competent(self):
        assert self.info.not_hired_and_not_competent == 3  # TN

    def test_not_hired_but_competent(self):
        assert self.info.not_hired_but_competent == 2  # FN

    def test_hired(self):
        assert self.info.hired == 3

    def test_not_hired(self):
        assert self.info.not_hired == 5

    def test_competent(self):
        assert self.info.competent == 4

    def test_not_competent(self):
        assert self.info.not_competent == 4

    def test_correct(self):
        assert self.info.correct == 5  # TP + TN

    def test_incorrect(self):
        assert self.info.incorrect == 3  # FP + FN


# ── GroupPredictionInformation rates ─────────────────────────────────────────


class TestGroupPredictionInformationRates:
    @pytest.fixture(autouse=True)
    def setup(self, df):
        self.info = GroupPredictionInformation(df)

    def test_accuracy(self):
        assert abs(self.info.accuracy - 5 / 8) < 1e-9

    def test_false_negative_rate(self):
        assert abs(self.info.false_negative_rate - 0.5) < 1e-9

    def test_false_positive_rate(self):
        assert abs(self.info.false_positive_rate - 0.25) < 1e-9

    def test_false_discovery_rate(self):
        assert abs(self.info.false_discovery_rate - 1 / 3) < 1e-9

    def test_false_omission_rate(self):
        assert abs(self.info.false_omission_rate - 0.4) < 1e-9

    def test_hired_rate(self):
        assert abs(self.info.hired_rate - 3 / 8) < 1e-9

    def test_competent_rate(self):
        assert abs(self.info.competent_rate - 0.5) < 1e-9

    def test_correct_rate(self):
        assert abs(self.info.correct_rate - 5 / 8) < 1e-9


# ── to_response serialisation ─────────────────────────────────────────────────


class TestGroupPredictionInformationToResponse:
    def test_returns_pydantic_model(self, df):
        from backend.api.types import GroupPredictionInformationResponse

        info = GroupPredictionInformation(df)
        response = info.to_response()
        assert isinstance(response, GroupPredictionInformationResponse)

    def test_response_values_match(self, df):
        info = GroupPredictionInformation(df)
        resp = info.to_response()
        assert resp.total == 8
        assert resp.hiredAndCompetent == 2
        assert abs(resp.falseNegativeRate - 0.5) < 1e-9
        assert abs(resp.falsePositiveRate - 0.25) < 1e-9

    def test_response_types_are_primitive(self, df):
        info = GroupPredictionInformation(df)
        resp = info.to_response()
        assert isinstance(resp.total, int)
        assert isinstance(resp.accuracy, float)
