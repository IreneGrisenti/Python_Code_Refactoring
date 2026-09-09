"""Responsible to read and save files."""

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

    logger.debug("Reading order data from %s", path)

    try:
        data = pd.read_csv(
            path, 
            dtype={
                "order_id": str, 
                "customer_id": str})
        
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Could not find file at {path}") from error

    logger.debug("Read %d rows", len(data))

    return data


def save_report(report: pd.DataFrame, output_folder: Path, report_key: str) -> None:

    try:
        filename = REPORT_FILENAMES[report_key]
    except KeyError as error:
            raise KeyError(f"Invalid report_key: {report_key}") from error
    
    path = output_folder / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    
    report.to_csv(path, index=False)
    
    logger.debug("Saved report %s to %s", filename, path)