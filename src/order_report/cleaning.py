"""Responsible for validating and cleaning the data before further processing."""

import pandas as pd
import logging


logger = logging.getLogger(__name__)


REQUIRED_COLUMNS = {
        "order_id",
        "order_date",
        "customer_id",
        "region",
        "product_category",
        "quantity",
        "unit_price",
        "discount",
        "returned",
    }

CATEGORICAL_COLUMNS_TO_NORMALIZE = ["region", "product_category"]

NUMERIC_COLUMNS_TO_NORMALIZE = ["quantity", "unit_price", "discount"]


def _check_required_columns(data: pd.DataFrame) -> None:
    """Controlls that all the required columns are present."""

    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing columns: {missing}")
    
    logger.debug("All the required columns were found: %s columns", len(REQUIRED_COLUMNS))


def normalize_categorical_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Fills missing values and normalizes string columns (region, product_category)."""

    copied_data = data.copy()
    for column in CATEGORICAL_COLUMNS_TO_NORMALIZE:
        copied_data[column] = copied_data[column].fillna("Unknown").astype(str).str.strip().str.title()

    logger.debug("Normalized columns: %s", ", ".join(CATEGORICAL_COLUMNS_TO_NORMALIZE))

    return copied_data


def _coerce_and_clean_column(column: pd.Series, fallback: float) -> pd.Series:
    """Converts to numerical, rejects negative values and fills in invalid/missing values with fallback."""

    numeric_column = pd.to_numeric(column, errors="coerce")
    numeric_column = numeric_column.where(numeric_column >= 0)

    return numeric_column.fillna(fallback)


def coerce_numeric_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Applies helper function to convert and fill missing values in quantity, unit_price och discount."""

    copied_data = data.copy()

    valid_unit_prices = pd.to_numeric(copied_data["unit_price"], errors="coerce")
    valid_unit_prices = valid_unit_prices.where(valid_unit_prices >= 0)
    unit_price_fallback = valid_unit_prices.median()

    copied_data["quantity"] = _coerce_and_clean_column(copied_data["quantity"], fallback=1)
    copied_data["unit_price"] = _coerce_and_clean_column(copied_data["unit_price"], fallback=unit_price_fallback)
    copied_data["discount"] = _coerce_and_clean_column(copied_data["discount"], fallback=0)

    logger.debug("Normalized columns: %s", ", ".join(NUMERIC_COLUMNS_TO_NORMALIZE))

    return copied_data


def convert_returned_to_boolean(data: pd.DataFrame) -> pd.DataFrame:
    """Converts the returned column to boolean."""

    copied_data = data.copy()

    copied_data["returned"] = (copied_data["returned"]
        .fillna("false")
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "yes", "1", "ja"])
    )

    logger.debug("Normalized column: returned")

    return copied_data


def clean_order_data(data: pd.DataFrame) -> pd.DataFrame:
    """Applies the validation and cleaning functions and returns a clean copia of the data datan.
    Raises ValueError if any required column is missing."""

    _check_required_columns(data)

    if len(data) == 0:
        raise ValueError("Empty data: there are no rows to clean")

    cleaned_data = normalize_categorical_columns(data)
    cleaned_data = coerce_numeric_columns(cleaned_data)
    cleaned_data = convert_returned_to_boolean(cleaned_data)

    return cleaned_data