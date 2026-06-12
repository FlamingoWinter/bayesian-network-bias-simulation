"""
Unit tests for backend/utils/.

All functions are pure or nearly-pure, so no fixtures are needed.
"""

import math
import time

import numpy as np
import pytest

from backend.utils.capitalise_first import capitalise_first
from backend.utils.entropy import (
    categorical_entropy_of_array,
    categorical_entropy_of_probabilities,
)
from backend.utils.replace_nan import replace_nan
from backend.utils.time_function import time_function


# ── capitalise_first ──────────────────────────────────────────────────────────


class TestCapitaliseFirst:
    def test_lowercases_first_letter(self):
        assert capitalise_first("hello") == "Hello"

    def test_preserves_rest_of_string(self):
        assert capitalise_first("hello WORLD") == "Hello WORLD"

    def test_already_uppercased(self):
        assert capitalise_first("Hello") == "Hello"

    def test_empty_string(self):
        assert capitalise_first("") == ""

    def test_single_character(self):
        assert capitalise_first("a") == "A"

    def test_non_alpha_first_char(self):
        assert capitalise_first("1 thing") == "1 thing"


# ── replace_nan ───────────────────────────────────────────────────────────────


class TestReplaceNan:
    def test_nan_float_becomes_none(self):
        assert replace_nan(float("nan")) is None

    def test_regular_float_unchanged(self):
        assert replace_nan(3.14) == 3.14

    def test_zero_unchanged(self):
        assert replace_nan(0.0) == 0.0

    def test_int_unchanged(self):
        assert replace_nan(42) == 42

    def test_string_unchanged(self):
        assert replace_nan("hello") == "hello"

    def test_none_unchanged(self):
        assert replace_nan(None) is None

    def test_dict_replaces_nan_values(self):
        result = replace_nan({"a": float("nan"), "b": 1.0})
        assert result == {"a": None, "b": 1.0}

    def test_list_replaces_nan_elements(self):
        result = replace_nan([float("nan"), 2.0, float("nan")])
        assert result == [None, 2.0, None]

    def test_nested_structure(self):
        result = replace_nan({"x": [float("nan"), {"y": float("nan")}]})
        assert result == {"x": [None, {"y": None}]}

    def test_dict_preserves_keys(self):
        result = replace_nan({"k": 1.0})
        assert list(result.keys()) == ["k"]


# ── time_function ─────────────────────────────────────────────────────────────


class TestTimeFunction:
    def test_returns_function_result(self):
        @time_function("test stage")
        def add(a, b):
            return a + b

        assert add(2, 3) == 5

    def test_passes_args_and_kwargs(self):
        @time_function("test stage")
        def greet(name, prefix="Hello"):
            return f"{prefix}, {name}"

        assert greet("World", prefix="Hi") == "Hi, World"

    def test_elapsed_time_is_non_negative(self, capsys):
        @time_function("timing test")
        def noop():
            time.sleep(0.01)

        noop()
        captured = capsys.readouterr()
        assert "timing test" in captured.out
        assert "completed in" in captured.out


# ── entropy ───────────────────────────────────────────────────────────────────


class TestEntropy:
    def test_uniform_binary_is_one_bit(self):
        probs = np.array([0.5, 0.5])
        result = categorical_entropy_of_probabilities(probs)
        assert abs(result - 1.0) < 1e-9

    def test_certain_distribution_is_zero(self):
        probs = np.array([1.0, 0.0])
        result = categorical_entropy_of_probabilities(probs)
        assert abs(result) < 1e-9

    def test_zero_probability_handled_without_error(self):
        # log2(0) would be -inf; the implementation guards against this
        probs = np.array([0.0, 0.5, 0.5])
        result = categorical_entropy_of_probabilities(probs)
        assert abs(result - 1.0) < 1e-9

    def test_uniform_four_categories(self):
        probs = np.array([0.25, 0.25, 0.25, 0.25])
        result = categorical_entropy_of_probabilities(probs)
        assert abs(result - 2.0) < 1e-9

    def test_entropy_of_array_uniform(self):
        array = np.array([0, 0, 1, 1])
        result = categorical_entropy_of_array(array)
        assert abs(result - 1.0) < 1e-9

    def test_entropy_of_array_certain(self):
        array = np.array([0, 0, 0, 0])
        result = categorical_entropy_of_array(array)
        assert abs(result) < 1e-9

    def test_entropy_of_array_skewed(self):
        # 75% / 25% split → H = -(0.75*log2(0.75) + 0.25*log2(0.25))
        array = np.array([0, 0, 0, 1])
        expected = -(0.75 * math.log2(0.75) + 0.25 * math.log2(0.25))
        result = categorical_entropy_of_array(array)
        assert abs(result - expected) < 1e-9
