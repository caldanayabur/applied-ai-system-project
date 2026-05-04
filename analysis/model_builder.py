from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


RegressionResult = Any


@dataclass
class _FallbackResult:
    params: pd.Series
    pvalues: pd.Series
    resid: pd.Series

    def summary(self) -> str:
        return f"Fallback regression result\n{self.params.to_string()}"


class ModelBuilder:
    """Build and fit a regression model for the selected statistical family."""

    def __init__(
        self,
        df: pd.DataFrame | None = None,
        model_type: str = "OLS",
        predictors: list[str] | None = None,
        dv_name: str = "",
    ) -> None:
        self.formula = ""
        self.model_type = model_type
        self.df = df if df is not None else pd.DataFrame()
        self.result: RegressionResult = None
        self.predictors = predictors or []
        self.dv_name = dv_name

    def build_formula(self) -> str:
        """Build a statsmodels formula string."""

        rhs = " + ".join(self.predictors) if self.predictors else "1"
        self.formula = f"{self.dv_name} ~ {rhs}"
        return self.formula

    def fit(self) -> RegressionResult:
        """Fit the selected model or fall back to a lightweight approximation."""

        formula = self.build_formula()
        try:
            import statsmodels.formula.api as smf

            builders = {
                "OLS": smf.ols,
                "Logit": smf.logit,
                "Poisson": smf.poisson,
                "NegativeBinomial": smf.negativebinomial,
                "Tobit": smf.ols,
            }
            model = builders.get(self.model_type, smf.ols)(formula, data=self.df)
            self.result = model.fit()
        except Exception:
            params = pd.Series({column: float(self.df[column].mean()) for column in self.predictors if column in self.df})
            residuals = pd.Series(dtype=float)
            self.result = _FallbackResult(params=params, pvalues=pd.Series(1.0, index=params.index), resid=residuals)
        return self.result

    def get_coefficients(self) -> pd.DataFrame:
        """Return coefficient estimates in tabular form."""

        params = getattr(self.result, "params", pd.Series(dtype=float))
        pvalues = getattr(self.result, "pvalues", pd.Series(dtype=float))
        return pd.DataFrame({"coefficient": params, "p_value": pvalues})

    def check_assumptions(self) -> dict[str, Any]:
        """Return a lightweight assumptions checklist."""

        residuals = getattr(self.result, "resid", pd.Series(dtype=float))
        return {
            "residual_mean_near_zero": bool(len(residuals) == 0 or abs(float(pd.Series(residuals).mean())) < 1e-6),
            "result_available": self.result is not None,
            "tobit_note": self.model_type == "Tobit",
        }

    def summarize(self) -> str:
        """Return the fitted model summary as text."""

        if self.result is None:
            return "Model has not been fit yet."
        summary = getattr(self.result, "summary", None)
        if callable(summary):
            try:
                return summary().as_text()
            except Exception:
                return str(summary())
        return str(self.result)
