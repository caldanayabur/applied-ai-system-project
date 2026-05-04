from __future__ import annotations

from pathlib import Path

from ai.copilot_advisor import CopilotAdvisor
from analysis.descriptive_analyzer import DescriptiveAnalyzer
from analysis.model_builder import ModelBuilder
from core.dataset_loader import DatasetLoader
from core.dv_analyzer import DVAnalyzer
from core.model_selector import ModelSelector
from output.report_generator import ReportGenerator


class StatBuddy:
    """High-level orchestration class for the StatBuddy pipeline."""

    def __init__(self) -> None:
        self.dataset_loader = DatasetLoader()
        self.dv_analyzer = DVAnalyzer()
        self.model_selector = ModelSelector()
        self.copilot_advisor = CopilotAdvisor()
        self.descriptive_analyzer = DescriptiveAnalyzer()
        self.model_builder = ModelBuilder()
        self.report_generator = ReportGenerator()
        self.confirmed_predictors: list[str] = []
        self.file_path: str = ""
        self.dv_name: str = ""

    def run(self, file_path: str, dv_name: str) -> str:
        """Execute the full pipeline for a dataset and dependent variable."""

        self.file_path = file_path
        self.dv_name = dv_name
        return self.execute_pipeline()

    def confirm_predictors(self, predictors: list[str]) -> list[str]:
        """Store predictor names after removing duplicates and missing columns."""

        available_columns = set(self.dataset_loader.column_names)
        confirmed: list[str] = []
        for predictor in predictors:
            if predictor in available_columns and predictor != self.dv_name and predictor not in confirmed:
                confirmed.append(predictor)
        if not confirmed:
            confirmed = [name for name in self.dataset_loader.column_names if name != self.dv_name]
        self.confirmed_predictors = confirmed
        return confirmed

    def execute_pipeline(self) -> str:
        """Run the StatBuddy pipeline from load to HTML report export."""

        df = self.dataset_loader.load(self.file_path)
        if not self.dataset_loader.validate():
            raise ValueError("The uploaded dataset must contain at least two columns.")

        self.dv_analyzer = DVAnalyzer(self.dv_name, df[self.dv_name])
        dv_type = self.dv_analyzer.detect_type()
        model_name = self.model_selector.select_model(dv_type)

        self.copilot_advisor.session = {"df": df}
        self.copilot_advisor.column_names = self.dataset_loader.column_names
        self.copilot_advisor.dv_name = self.dv_name
        self.copilot_advisor.connect()
        predictors = self.confirm_predictors(self.copilot_advisor.suggest_predictors())

        self.descriptive_analyzer = DescriptiveAnalyzer(df, predictors, self.dv_name)
        descriptive_tables = self.descriptive_analyzer.generate_tables()
        figures = self.descriptive_analyzer.plot_distributions()

        self.model_builder = ModelBuilder(df, model_name, predictors, self.dv_name)
        self.model_builder.fit()

        self.report_generator.report_data = {
            "dataset_name": Path(self.file_path).name,
            "dv_name": self.dv_name,
            "model_name": model_name,
            "model_justification": self.model_selector.get_justification(),
            "predictors": self.copilot_advisor.justify_predictors(),
            "descriptive_tables": descriptive_tables,
            "figures": figures,
            "coefficients": self.model_builder.get_coefficients(),
            "assumptions": self.model_builder.check_assumptions(),
            "model_summary": self.model_builder.summarize(),
            "selected_predictors": predictors,
            "dv_summary": self.dv_analyzer.summarize(),
            "dv_type": dv_type,
        }
        self.report_generator.include_plots(figures)
        self.report_generator.compile_data()
        self.report_generator.export(self.report_generator.output_path)
        return self.report_generator.output_path
