from __future__ import annotations

import pandas as pd
import pytest

from analysis.model_builder import ModelBuilder


@pytest.fixture
def frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "y": [1, 2, 3, 4, 5, 6],
            "x1": [2, 3, 4, 5, 6, 7],
            "x2": [1, 0, 1, 0, 1, 0],
        }
    )


@pytest.fixture
def builder(frame: pd.DataFrame) -> ModelBuilder:
    return ModelBuilder(frame, "OLS", ["x1", "x2"], "y")


def test_build_formula(builder: ModelBuilder) -> None:
    assert builder.build_formula() == "y ~ x1 + x2"


def test_fit_and_coefficients(builder: ModelBuilder) -> None:
    result = builder.fit()
    coefficients = builder.get_coefficients()
    assert result is not None
    assert not coefficients.empty


def test_assumptions_and_summary(builder: ModelBuilder) -> None:
    builder.fit()
    assumptions = builder.check_assumptions()
    assert {"residual_mean_near_zero", "result_available", "tobit_note"}.issubset(assumptions)
    assert isinstance(builder.summarize(), str)
