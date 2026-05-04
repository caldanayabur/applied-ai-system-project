from __future__ import annotations

import pytest

from core.model_selector import ModelSelector


@pytest.fixture
def selector() -> ModelSelector:
    return ModelSelector()


def test_select_model_returns_expected_name(selector: ModelSelector) -> None:
    assert selector.select_model("binary") == "Logit"


def test_get_justification_is_populated(selector: ModelSelector) -> None:
    selector.select_model("count")
    assert selector.get_justification().strip() != ""


def test_get_model_family_matches_rule(selector: ModelSelector) -> None:
    selector.select_model("continuous_normal")
    assert selector.get_model_family() == "gaussian"
