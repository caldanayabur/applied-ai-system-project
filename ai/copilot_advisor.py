from __future__ import annotations

import asyncio
import importlib
import inspect
from typing import Any

import pandas as pd


class CopilotAdvisor:
    """Ask GitHub Copilot for ranked predictor suggestions with a fallback."""

    def __init__(self, session: Any = None, column_names: list[str] | None = None, dv_name: str = "") -> None:
        self.session = session
        self.column_names = column_names or []
        self.dv_name = dv_name
        self.suggested_predictors: list[str] = []

    def connect(self) -> bool:
        """Attempt to connect to the GitHub Copilot SDK."""

        for module_name in ("github_copilot_sdk", "githubcopilot_sdk", "copilot_sdk"):
            try:
                self.session = importlib.import_module(module_name)
                return True
            except Exception:
                continue
        return False

    def suggest_predictors(self) -> list[str]:
        """Ask Copilot for ranked predictor suggestions or use correlations."""

        prompt = self._build_prompt()
        handler = self._get_session_handler()
        if handler is not None:
            response = handler(prompt)
            if inspect.isawaitable(response):
                response = asyncio.run(response)
            suggestions = self._parse_response(response)
            if suggestions:
                self.suggested_predictors = suggestions
                return self.suggested_predictors
        self.suggested_predictors = self._fallback_predictors()
        return self.suggested_predictors

    def explain_model(self) -> str:
        """Describe the current predictor plan in plain English."""

        predictors = ", ".join(self.suggested_predictors) or "the strongest available predictors"
        return f"Copilot recommends modeling {self.dv_name} with {predictors}."

    def justify_predictors(self) -> dict[str, str]:
        """Return a simple justification for each selected predictor."""

        if isinstance(self.session, dict) and isinstance(self.session.get("df"), pd.DataFrame):
            df = self.session["df"]
            if self.dv_name in df.columns:
                target = pd.to_numeric(df[self.dv_name], errors="coerce")
                correlations = df.select_dtypes(include="number").drop(columns=[self.dv_name], errors="ignore").corrwith(target).abs()
                return {name: f"Highest absolute correlation with {self.dv_name}: {correlations.get(name, float('nan')):.3f}" for name in self.suggested_predictors}
        return {name: "Selected as a plausible predictor from the available columns." for name in self.suggested_predictors}

    def _build_prompt(self) -> str:
        return f"Rank predictors for dependent variable {self.dv_name} using columns: {', '.join(self.column_names)}. Provide brief justifications."

    def _get_session_handler(self) -> Any:
        for attribute in ("prompt", "suggest", "chat"):
            handler = getattr(self.session, attribute, None)
            if callable(handler):
                return handler
        return None

    def _parse_response(self, response: Any) -> list[str]:
        if isinstance(response, list):
            return [str(item).strip() for item in response if str(item).strip()]
        text = str(response or "")
        lines = [line.strip("- *\t ") for line in text.splitlines()]
        return [line for line in lines if line and line in self.column_names and line != self.dv_name]

    def _fallback_predictors(self) -> list[str]:
        df = self.session.get("df") if isinstance(self.session, dict) else None
        if isinstance(df, pd.DataFrame) and self.dv_name in df.columns:
            numeric = df.select_dtypes(include="number")
            if self.dv_name in numeric.columns:
                correlations = numeric.drop(columns=[self.dv_name], errors="ignore").corrwith(numeric[self.dv_name]).abs().sort_values(ascending=False)
                ranked = [name for name in correlations.index if name in self.column_names and name != self.dv_name]
                if ranked:
                    return ranked[:3]
        return [name for name in self.column_names if name != self.dv_name][:3]
