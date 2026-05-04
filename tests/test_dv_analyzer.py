from __future__ import annotations

import pandas as pd
import pytest

from core.dv_analyzer import DVAnalyzer


@pytest.fixture
def series_map() -> dict[str, pd.Series]:
    return {
        "binary": pd.Series([0, 1, 0, 1, 1, 0]),
        "count": pd.Series([0, 1, 2, 1, 3, 4]),
        "continuous": pd.Series([1.2, 2.3, 3.4, 4.1, 5.0, 6.2]),
    }


@pytest.fixture
def analyzer(series_map: dict[str, pd.Series]) -> DVAnalyzer:
    return DVAnalyzer("y", series_map["continuous"])


def test_detect_type_identifies_binary_and_count(series_map: dict[str, pd.Series]) -> None:
    assert DVAnalyzer("y", series_map["binary"]).detect_type() == "binary"
    assert DVAnalyzer("y", series_map["count"]).detect_type() == "count"


def test_normality_and_summary(analyzer: DVAnalyzer) -> None:
    normality = analyzer.test_normality()
    summary = analyzer.summarize()
    assert set(normality) == {"statistic", "p_value"}
    assert {"mean", "std", "min", "max", "skewness", "kurtosis"}.issubset(summary)


def test_overdispersion_and_histogram(series_map: dict[str, pd.Series]) -> None:
    analyzer = DVAnalyzer("y", series_map["count"])
    assert analyzer.check_overdispersion() in {True, False}
    assert analyzer.plot_histogram() is not None
