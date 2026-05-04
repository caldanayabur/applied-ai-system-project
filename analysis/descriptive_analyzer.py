from __future__ import annotations

from typing import Any

import pandas as pd

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
except Exception:  # pragma: no cover - optional dependency fallback
    plt = None
    Figure = Any


class DescriptiveAnalyzer:
    """Generate descriptive statistics and simple visualizations."""

    def __init__(self, df: pd.DataFrame | None = None, predictors: list[str] | None = None, dv_name: str = "") -> None:
        self.df = df if df is not None else pd.DataFrame()
        self.predictors = predictors or []
        self.dv_name = dv_name
        self.summary_stats: dict[str, dict[str, Any]] = {}

    def analyze_numeric(self, col: str) -> dict[str, Any]:
        """Summarize a numeric column and produce a histogram."""

        series = pd.to_numeric(self.df[col], errors="coerce").dropna()
        figure = None
        if plt is not None:
            figure, axis = plt.subplots(figsize=(5, 3))
            axis.hist(series, bins=10, color="#1f2937", edgecolor="white")
            axis.set_title(col)
            figure.tight_layout()
        summary = {
            "mean": float(series.mean()) if len(series) else float("nan"),
            "median": float(series.median()) if len(series) else float("nan"),
            "std": float(series.std(ddof=1)) if len(series) > 1 else float("nan"),
            "skewness": float(series.skew()) if len(series) > 2 else float("nan"),
            "histogram": figure,
        }
        self.summary_stats[col] = summary
        return summary

    def analyze_categorical(self, col: str) -> dict[str, Any]:
        """Summarize a categorical column with counts and percentages."""

        counts = self.df[col].astype(str).value_counts(dropna=False)
        frequency_table = counts.rename_axis(col).reset_index(name="count")
        frequency_table["frequency"] = frequency_table["count"] / max(len(self.df), 1)
        figure = None
        if plt is not None:
            figure, axis = plt.subplots(figsize=(5, 3))
            counts.head(10).plot(kind="bar", ax=axis, color="#2563eb")
            axis.set_title(col)
            figure.tight_layout()
        summary = {"value_counts": counts, "frequency_table": frequency_table, "figure": figure}
        self.summary_stats[col] = summary
        return summary

    def correlation_matrix(self) -> pd.DataFrame:
        """Return the correlation matrix for numeric predictors and the DV."""

        columns = [name for name in self.predictors + [self.dv_name] if name in self.df.columns]
        return self.df[columns].select_dtypes(include="number").corr()

    def plot_distributions(self) -> list[Figure]:
        """Create distribution plots for all configured predictors."""

        figures: list[Figure] = []
        for column in self.predictors:
            if pd.api.types.is_numeric_dtype(self.df[column]):
                figures.append(self.analyze_numeric(column)["histogram"])
            else:
                figures.append(self.analyze_categorical(column)["figure"])
        return [figure for figure in figures if figure is not None]

    def generate_tables(self) -> dict[str, dict[str, Any]]:
        """Automatically analyze each predictor and return the collected tables."""

        tables: dict[str, dict[str, Any]] = {}
        for column in self.predictors:
            tables[column] = (
                self.analyze_numeric(column)
                if pd.api.types.is_numeric_dtype(self.df[column])
                else self.analyze_categorical(column)
            )
        return tables
