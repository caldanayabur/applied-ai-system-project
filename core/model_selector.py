from __future__ import annotations

import json
from pathlib import Path


class ModelSelector:
    """Map dependent-variable types to statistical model recommendations."""

    def __init__(self) -> None:
        self.dv_type: str = ""
        self.selected_model: str = ""
        self.model_rules = self._load_rules()
        self.justification: str = ""

    def select_model(self, dv_type: str) -> str:
        """Select a model for the supplied dependent-variable type."""

        self.dv_type = dv_type
        rule = self.model_rules.get(dv_type, self.model_rules["continuous_normal"])
        self.selected_model = rule["model"] or "OLS"
        self.justification = rule["justification"]
        return self.selected_model

    def get_justification(self) -> str:
        """Return the model-selection explanation."""

        return self.justification

    def get_model_family(self) -> str:
        """Return the model family for the selected model, when available."""

        rule = self.model_rules.get(self.dv_type, self.model_rules["continuous_normal"])
        return str(rule.get("family") or "gaussian")

    def _load_rules(self) -> dict:
        path = Path(__file__).resolve().parents[1] / "knowledge" / "model_rules.json"
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
