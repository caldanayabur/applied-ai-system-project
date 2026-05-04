from __future__ import annotations

import pandas as pd
import pytest

from ai.copilot_advisor import CopilotAdvisor


@pytest.fixture
def advisor() -> CopilotAdvisor:
    frame = pd.DataFrame(
        {
            "y": [1, 2, 3, 4, 5, 6],
            "x1": [2, 3, 4, 5, 6, 7],
            "x2": [1, 1, 0, 0, 1, 0],
            "x3": [10, 9, 8, 7, 6, 5],
        }
    )
    return CopilotAdvisor(session={"df": frame}, column_names=list(frame.columns), dv_name="y")


def test_connect_handles_missing_sdk(advisor: CopilotAdvisor) -> None:
    assert advisor.connect() in {True, False}


def test_suggest_predictors_uses_fallback(advisor: CopilotAdvisor) -> None:
    predictors = advisor.suggest_predictors()
    assert predictors and "y" not in predictors


def test_explain_and_justify(advisor: CopilotAdvisor) -> None:
    advisor.suggest_predictors()
    explanation = advisor.explain_model()
    justifications = advisor.justify_predictors()
    assert isinstance(explanation, str) and explanation.strip() != ""
    assert isinstance(justifications, dict)
