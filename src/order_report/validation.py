"""Ansvarar för att kontrollera och städa order-datan innan den bearbetas vidare."""

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


def check_required_columns(data: pd.DataFrame) -> None:
    """Kontrollerar att nödvändiga kolumner finns."""

    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing columns: {missing}")
    
    logger.info("Alla nödvändiga kolumner hittades: %s kolumner.", len(REQUIRED_COLUMNS))


def normalize_categorical_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Fyller saknade värden och normaliserar strängkolumner (region, product_category)."""

    copied_data = data.copy()
    for column in CATEGORICAL_COLUMNS_TO_NORMALIZE:
        copied_data[column] = copied_data[column].fillna("Unknown").astype(str).str.strip().str.title()

    logger.info("Normaliserade kolumner: %s.", ", ".join(CATEGORICAL_COLUMNS_TO_NORMALIZE))

    return copied_data


def coerce_numeric_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Konverterar och fyller i saknade värden för quantity, unit_price och discount."""

    copied_data = data.copy()

    copied_data["quantity"] = pd.to_numeric(copied_data["quantity"], errors="coerce").fillna(1)

    copied_data["unit_price"] = pd.to_numeric(copied_data["unit_price"], errors="coerce")
    copied_data["unit_price"] = copied_data["unit_price"].fillna(copied_data["unit_price"].median())

    copied_data["discount"] = pd.to_numeric(copied_data["discount"], errors="coerce").fillna(0)

    logger.info("Normaliserade kolumner: %s.", ", ".join(NUMERIC_COLUMNS_TO_NORMALIZE))

    return copied_data


def convert_returned_to_boolean(data: pd.DataFrame) -> pd.DataFrame:
    """Konverterar kolumnen returned till boolean."""

    copied_data = data.copy()

    copied_data["returned"] = (copied_data["returned"]
        .fillna("false")
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "yes", "1", "ja"])
    )

    logger.info("Normaliserade kolumn returned.")

    return copied_data


def validate_order_data(data: pd.DataFrame) -> pd.DataFrame:
    """Applicerar valideringsfunktioner och returnerar en ren, validerad copia av datan.
    Höjer ValueError om nödvändiga kolumner saknas."""

    logger.info("Validering startar.")

    check_required_columns(data)

    validated_data = normalize_categorical_columns(data)
    validated_data = coerce_numeric_columns(validated_data)
    validated_data = convert_returned_to_boolean(validated_data)

    logger.info("Validering genomfört.")

    return validated_data