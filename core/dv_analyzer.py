from __future__ import annotations

from math import isnan
from typing import Any

import numpy as np
import pandas as pd

try:
    import matplotlib

    matplotlib.use("Agg")
    from scipy import stats
except Exception:  # pragma: no cover - optional dependency fallback
    stats = None

try:
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
except Exception:  # pragma: no cover - optional dependency fallback
    plt = None
    Figure = Any


class DVAnalyzer:
    """Inspect the dependent variable and infer an appropriate model shape."""

    def __init__(self, dv_name: str = "", dv_series: pd.Series | None = None) -> None:
        self.dv_name = dv_name
        self.dv_series = dv_series if dv_series is not None else pd.Series(dtype=float)
        self.detected_type = ""
        self.distribution_stats: dict[str, float] = {}

    def detect_type(self) -> str:
        """Infer the dependent-variable type from simple statistical rules."""

        series = self.dv_series.dropna()
        if series.empty:
            self.detected_type = "continuous_normal"
        elif series.nunique() <= 2:
            self.detected_type = "binary"
        elif self._looks_censored(series):
            self.detected_type = "censored"
        elif self._is_count_like(series):
            self.detected_type = "count"
        else:
            normality = self.test_normality().get("p_value", float("nan"))
            skewness = self.summarize().get("skewness", 0.0)
            self.detected_type = (
                "continuous_normal" if (not isnan(normality) and normality >= 0.05 and abs(skewness) < 1) else "continuous_skewed"
            )
        return self.detected_type

    def test_normality(self) -> dict[str, float]:
        """Run the Shapiro-Wilk test when available."""

        series = self.dv_series.dropna()
        if len(series) < 3 or stats is None:
            return {"statistic": float("nan"), "p_value": float("nan")}
        try:
            statistic, p_value = stats.shapiro(series.astype(float).to_numpy())
        except Exception:
            statistic, p_value = float("nan"), float("nan")
        return {"statistic": float(statistic), "p_value": float(p_value)}

    def check_overdispersion(self) -> bool:
        """Return True when the variance is larger than the mean."""

        series = self.dv_series.dropna().astype(float)
        return bool(len(series) and series.var(ddof=1) > series.mean())

    def plot_histogram(self) -> Figure:
        """Create a histogram of the dependent variable."""

        if plt is None:
            raise RuntimeError("matplotlib is required for plotting")
        figure, axis = plt.subplots(figsize=(5, 3))
        axis.hist(self.dv_series.dropna(), bins=10, color="#2b6cb0", edgecolor="white")
        axis.set_title(f"{self.dv_name} distribution")
        axis.set_xlabel(self.dv_name)
        axis.set_ylabel("Frequency")
        figure.tight_layout()
        return figure

    def summarize(self) -> dict[str, float]:
        """Compute core summary statistics for the dependent variable."""

        series = self.dv_series.dropna().astype(float)
        summary = {
            "mean": float(series.mean()) if len(series) else float("nan"),
            "std": float(series.std(ddof=1)) if len(series) > 1 else float("nan"),
            "min": float(series.min()) if len(series) else float("nan"),
            "max": float(series.max()) if len(series) else float("nan"),
            "skewness": float(series.skew()) if len(series) > 2 else float("nan"),
            "kurtosis": float(series.kurt()) if len(series) > 3 else float("nan"),
        }
        self.distribution_stats = summary
        return summary

    def _is_count_like(self, series: pd.Series) -> bool:
        numeric = pd.to_numeric(series, errors="coerce").dropna()
        return bool(len(numeric) and (numeric >= 0).all() and np.allclose(numeric, np.round(numeric)))

    def _looks_censored(self, series: pd.Series) -> bool:
        numeric = pd.to_numeric(series, errors="coerce").dropna()
        zero_share = float((numeric == 0).mean()) if len(numeric) else 0.0
        return bool(len(numeric) > 4 and zero_share >= 0.3 and numeric.nunique() > 3)
