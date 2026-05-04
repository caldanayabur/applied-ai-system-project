from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from jinja2 import Environment, FileSystemLoader
except Exception:  # pragma: no cover - optional dependency fallback
    Environment = None
    FileSystemLoader = None

try:
    from matplotlib.figure import Figure
except Exception:  # pragma: no cover - optional dependency fallback
    Figure = Any


class ReportGenerator:
    """Render the final HTML report from StatBuddy analysis artifacts."""

    def __init__(self, template_path: str = "templates/report.html", output_path: str = "output/report.html") -> None:
        self.template_path = template_path
        self.output_path = output_path
        self.report_data: dict[str, Any] = {}

    def compile_data(self) -> dict[str, Any]:
        """Normalize the stored report data for HTML rendering."""

        compiled = self._serialize(self.report_data)
        self.report_data = compiled
        return compiled

    def render_html(self) -> str:
        """Render the report to an HTML string using Jinja2 when available."""

        data = self.compile_data()
        if Environment is None or FileSystemLoader is None:
            return self._fallback_html(data)
        template_file = Path(self.template_path)
        environment = Environment(loader=FileSystemLoader(str(template_file.parent)), autoescape=True)
        return environment.get_template(template_file.name).render(**data)

    def export(self, path: str | None = None) -> str:
        """Write the HTML report to disk and return the output path."""

        output_file = Path(path or self.output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(self.render_html(), encoding="utf-8")
        return str(output_file)

    def include_plots(self, figures: list[Figure]) -> list[str]:
        """Convert matplotlib figures to base64-encoded PNG images."""

        return [self._figure_to_base64(figure) for figure in figures if figure is not None]

    def _serialize(self, value: Any) -> Any:
        if isinstance(value, pd.DataFrame):
            return value.to_html(index=False, classes="data-table", border=0)
        if isinstance(value, pd.Series):
            return value.to_frame(name="value").to_html(classes="data-table", border=0)
        if isinstance(value, Figure):
            return self._figure_to_base64(value)
        if isinstance(value, dict):
            return {key: self._serialize(item) for key, item in value.items()}
        if isinstance(value, list):
            return [self._serialize(item) for item in value]
        return value

    def _figure_to_base64(self, figure: Figure) -> str:
        buffer = BytesIO()
        figure.savefig(buffer, format="png", bbox_inches="tight")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def _fallback_html(self, data: dict[str, Any]) -> str:
        rows = "".join(f"<tr><th>{key}</th><td>{value}</td></tr>" for key, value in data.items())
        return f"<html><body><h1>StatBuddy Report</h1><table>{rows}</table></body></html>"
