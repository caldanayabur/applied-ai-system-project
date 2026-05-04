from __future__ import annotations

from pathlib import Path

import pandas as pd


class DatasetLoader:
    """Load and inspect user-uploaded CSV datasets."""

    def __init__(self) -> None:
        self.file_path: str = ""
        self.df: pd.DataFrame = pd.DataFrame()
        self.column_names: list[str] = []
        self.n_rows: int = 0
        self.n_cols: int = 0

    def load(self, file_path: str) -> pd.DataFrame:
        """Load a CSV file into memory."""

        self.file_path = str(file_path)
        self.df = pd.read_csv(Path(file_path))
        self.column_names = list(self.df.columns)
        self.n_rows, self.n_cols = self.df.shape
        return self.df

    def preview(self) -> pd.DataFrame:
        """Return the first five rows of the loaded dataset."""

        return self.df.head(5)

    def get_column_types(self) -> dict[str, str]:
        """Return a mapping of column names to pandas dtype strings."""

        return {name: str(dtype) for name, dtype in self.df.dtypes.items()}

    def validate(self) -> bool:
        """Check that the dataset is usable for analysis."""

        return not self.df.empty and self.n_cols >= 2
