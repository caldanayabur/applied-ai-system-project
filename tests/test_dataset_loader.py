from __future__ import annotations

import pandas as pd
import pytest

from core.dataset_loader import DatasetLoader


@pytest.fixture
def sample_csv(tmp_path):
    frame = pd.DataFrame({"y": [1, 2, 3, 4, 5, 6], "x1": [10, 11, 12, 13, 14, 15], "x2": [0, 1, 0, 1, 0, 1]})
    path = tmp_path / "sample.csv"
    frame.to_csv(path, index=False)
    return path, frame


@pytest.fixture
def loader() -> DatasetLoader:
    return DatasetLoader()


def test_load_sets_metadata(loader: DatasetLoader, sample_csv) -> None:
    path, frame = sample_csv
    loaded = loader.load(str(path))
    assert loaded.equals(frame)
    assert loader.n_rows == 6 and loader.n_cols == 3


def test_preview_returns_first_rows(loader: DatasetLoader, sample_csv) -> None:
    path, _ = sample_csv
    loader.load(str(path))
    assert len(loader.preview()) == 5


def test_validate_and_types(loader: DatasetLoader, sample_csv) -> None:
    path, _ = sample_csv
    loader.load(str(path))
    assert loader.validate() is True
    assert loader.get_column_types()["y"] in {"int64", "float64"}
