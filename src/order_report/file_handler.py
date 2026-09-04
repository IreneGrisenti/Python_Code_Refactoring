"""Ansvarar för att läsa indata och spara rapporter."""

from pathlib import Path
import pandas as pd
import logging

REPORT_FILENAMES = {
    "overview": "overview.csv",
    "sales_by_category": "sales_by_category.csv",
    "sales_by_region": "sales_by_region.csv",
    "returns_by_category": "returns_by_category.csv"
}

logger = logging.getLogger(__name__)

def load_data(path: Path) -> pd.DataFrame:
    logger.info("Läser order data från %s", path)
    return pd.read_csv(path)

def save_report(report: pd.DataFrame, output_folder: Path, report_key: str) -> None:
    filename = REPORT_FILENAMES[report_key]
    path = output_folder / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(path, index=False)
    logger.info("Sparade rapport %s till %s", filename, path)