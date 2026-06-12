"""
Unit tests for MitigationBiasAnalysis (mitigation_analysis.py).

Uses the same hand-computed 8-row DataFrame as test_prediction_metrics.py.
The fixture has two groups (0 and 1) so we can verify per-group breakdowns
and the to_response() serialisation contract.
"""

import pytest

from backend.simulation.measure_bias.mitigation_analysis import MitigationBiasAnalysis


@pytest.fixture()
def analysis(known_confusion_df, binary_characteristic):
    """MitigationBiasAnalysis over the known 8-row fixture."""
    return MitigationBiasAnalysis(known_confusion_df, binary_characteristic)


# ── Construction ──────────────────────────────────────────────────────────────


class TestMitigationBiasAnalysisConstruction:
    def test_general_exists(self, analysis):
        assert analysis.general is not None

    def test_by_group_has_both_groups(self, analysis, binary_characteristic):
        expected_groups = set(binary_characteristic.category_names)
        assert set(analysis.by_group.keys()) == expected_groups

    def test_general_total_is_full_dataset(self, analysis, known_confusion_df):
        assert analysis.general.total == len(known_confusion_df)

    def test_group_totals_sum_to_total(self, analysis):
        group_total = sum(g.total for g in analysis.by_group.values())
        assert group_total == analysis.general.total


# ── Per-group values ──────────────────────────────────────────────────────────
#
# From known_confusion_df:
#   group 0 rows (indices 0,2,4,5):  actual=[1,1,0,0]  predicted=[1,0,1,0]
#     → TP=1 FN=1 FP=1 TN=1  → FNR=0.5, FPR=0.5, FDR=0.5, FOR=0.5
#   group 1 rows (indices 1,3,6,7):  actual=[1,1,0,0]  predicted=[1,0,0,0]
#     → TP=1 FN=1 FP=0 TN=2  → FNR=0.5, FPR=0.0, FDR=0.0, FOR=1/3


class TestMitigationBiasAnalysisPerGroup:
    def test_group_male_total(self, analysis):
        assert analysis.by_group["male"].total == 4

    def test_group_female_total(self, analysis):
        assert analysis.by_group["female"].total == 4

    def test_group_male_fnr(self, analysis):
        assert abs(analysis.by_group["male"].false_negative_rate - 0.5) < 1e-9

    def test_group_female_fpr(self, analysis):
        assert abs(analysis.by_group["female"].false_positive_rate - 0.0) < 1e-9

    def test_group_male_fpr(self, analysis):
        assert abs(analysis.by_group["male"].false_positive_rate - 0.5) < 1e-9


# ── to_response ───────────────────────────────────────────────────────────────


class TestMitigationBiasAnalysisToResponse:
    def test_returns_recruiter_bias_analysis_response(self, analysis):
        from backend.api.schemas import RecruiterBiasAnalysisResponse

        response = analysis.to_response()
        assert isinstance(response, RecruiterBiasAnalysisResponse)

    def test_response_has_general_and_by_group(self, analysis):
        response = analysis.to_response()
        assert response.general is not None
        assert len(response.byGroup) == 2

    def test_response_group_keys_match(self, analysis, binary_characteristic):
        response = analysis.to_response()
        assert set(response.byGroup.keys()) == set(binary_characteristic.category_names)

    def test_response_general_total(self, analysis):
        response = analysis.to_response()
        assert response.general.total == 8
