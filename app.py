from __future__ import annotations

import csv
import tempfile
from pathlib import Path

import streamlit as st

from core.statbuddy import StatBuddy


def _extract_column_names(file_path: Path) -> list[str]:
    """Read the CSV header for the dependent-variable selector."""

    with file_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        return next(reader, [])


def main() -> None:
    """Render the StatBuddy Streamlit app."""

    st.title("🤖 StatBuddy — Your Statistics Peer")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if not uploaded_file:
        return

    temp_path = Path(tempfile.gettempdir()) / f"statbuddy_{uploaded_file.name}"
    temp_path.write_bytes(uploaded_file.getbuffer())
    column_names = _extract_column_names(temp_path)
    if not column_names:
        st.error("No columns were found in the uploaded CSV.")
        return

    dv_name = st.selectbox("Select the dependent variable", column_names)
    if st.button("Run StatBuddy"):
        statbuddy = StatBuddy()
        report_path = statbuddy.run(str(temp_path), dv_name)
        st.success(f"StatBuddy finished. Report saved to {report_path}")
        st.write(f"Confirmed predictors: {', '.join(statbuddy.confirmed_predictors) or 'None'}")


if __name__ == "__main__":
    main()
