"""
Tests for file_handler.py.

Checks that file_handler.py. functions perform corretly with the following tests:
1. load_data reads a .csv file correctly.
2. load_data raises FileNotFoundError when a given path doesn't exist.
3. save_report writes the right content into the right file.
4. save_report raises KeyError when given an unrecognized file name.
"""

from pathlib import Path
import pandas as pd
import pytest
from order_report.file_handler import (
    load_data,
    save_report
)


def test_load_data_reads_csv(tmp_path: Path) -> None:
    """"Verifies that load_data correctly reads a .csv file.""" 

    csv_path = tmp_path / "order.csv"
    csv_path.write_text(
        "order_id,order_date,customer_id,region"
        "\n00001,2026-01-04,C018,South"
        "\n00002,2026-03-17,C028,North",
        encoding="utf-8"
    )

    expected = pd.DataFrame(
        {
            "order_id": ["00001", "00002"],
            "order_date": ["2026-01-04", "2026-03-17"],
            "customer_id": ["C018", "C028"],
            "region": ["South", "North"],
        }
    )

    result = load_data(csv_path)

    pd.testing.assert_frame_equal(expected, result)


def test_load_data_missing_file(tmp_path: Path) -> None:
    """"Verifies that load_data raises FileNotFoundError when the given path does not exist."""

    csv_path = tmp_path / "order.csv"

    with pytest.raises(
        FileNotFoundError,
        match= "Could not find file"
        ):
        load_data(csv_path)


def test_save_report_writes_csv(tmp_path: Path) -> None:
    """Verifies that save_report writes the report to the correct file with correct content."""

    report = pd.DataFrame({
        "metric": ["total_sales", "order_count"],
        "value": [150.0, 2.0],
    })

    save_report(report, tmp_path, "overview")

    saved_path = tmp_path / "overview.csv"

    result = pd.read_csv(saved_path)
    pd.testing.assert_frame_equal(result, report)


def test_save_report_invalid_report_key(tmp_path: Path) -> None:
    """Verifies that save_report raises KeyError when given an unrecognized report_key."""

    report = pd.DataFrame({"metric": ["total_sales"], "value": [100.0]})

    with pytest.raises(
        KeyError,
        match= "Invalid report_key"
        ):
        save_report(report, tmp_path, "not_a_real_key")