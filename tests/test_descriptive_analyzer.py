from __future__ import annotations

import pandas as pd
import pytest

from analysis.descriptive_analyzer import DescriptiveAnalyzer


@pytest.fixture
def frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "y": [1, 2, 3, 4, 5, 6],
            "x_num": [10, 11, 12, 13, 14, 15],
            "x_cat": ["a", "b", "a", "c", "b", "a"],
        }
    )


@pytest.fixture
def analyzer(frame: pd.DataFrame) -> DescriptiveAnalyzer:
    return DescriptiveAnalyzer(frame, ["x_num", "x_cat"], "y")


def test_analyze_numeric_returns_stats(analyzer: DescriptiveAnalyzer) -> None:
    result = analyzer.analyze_numeric("x_num")
    assert {"mean", "median", "std", "skewness", "histogram"}.issubset(result)


def test_analyze_categorical_returns_frequency_table(analyzer: DescriptiveAnalyzer) -> None:
    result = analyzer.analyze_categorical("x_cat")
    assert "frequency_table" in result and len(result["value_counts"]) == 3


def test_correlation_and_generation(analyzer: DescriptiveAnalyzer) -> None:
    tables = analyzer.generate_tables()
    assert "x_num" in tables and "x_cat" in tables
    assert analyzer.correlation_matrix().shape[0] >= 1
    assert len(analyzer.plot_distributions()) >= 1
