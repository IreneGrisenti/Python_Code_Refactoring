""" 
Tests for cleaning.py.

Checks that cleaning.py functions perform correctly with the following tests:
1. All required columns are present: does not raise an error.
2. Multiple missing columns: raises ValueError naming each missing column.
3. Categorical columns (region, product_category) are trimmed, title-cased and missing values filled with "Unknown".
4. Numeric strings are converted correctly and missing values are filled with the right default per column.
5. Invalid strings and negative values are treated as invalid and filled with the same defaults as missing values.
6. Recognized true variants, casing, whitespace and missing values are converted correctly to boolean.
7. Full cleaning pipeline on mixed, unclean data produces correctly cleaned output across all columns.
8. Empty dataframe raises ValueError instead of silently passing through.
9. clean_order_data does not mutate the original input dataframe.
"""

import pandas as pd
import pytest

from order_report.cleaning import (
    _check_required_columns, 
    normalize_categorical_columns,
    coerce_numeric_columns,
    convert_returned_to_boolean,
    clean_order_data
)


def test_check_required_columns_all_present() -> None:
    """Verifies the normal behavior of the function: when all the required columns are present no exception is raised."""

    data = pd.DataFrame(columns=[
        "order_id",
        "order_date",
        "customer_id",
        "region",
        "product_category",
        "quantity",
        "unit_price",
        "discount",
        "returned",
    ])

    result = _check_required_columns(data)

    assert result is None


def test_check_required_columns_multiple_missing() -> None:
    """Verifies that ValueError is raised in case of missing required columns, informing on which specific column is missing."""

    data = pd.DataFrame(columns=[
            "order_id",
            "order_date",
            "customer_id",
            "region",
            "product_category",
            "returned",
        ])

    with pytest.raises(
        ValueError,
        match="Missing columns: discount, quantity, unit_price"
    ): _check_required_columns(data)


def test_normalize_categorical_columns_cleans_and_fills_missing() -> None:
    """Verifies that region and product_category are trimmed, title-cased and missing values are filled with 'Unknown'."""

    data = pd.DataFrame({
        "region": ["South  ", "north", None],
        "product_category": ["ELECTRONICS", "Electronics", "  Electronics"],
    })

    expected =  pd.DataFrame({
        "region": ["South", "North", "Unknown"],
        "product_category": ["Electronics", "Electronics", "Electronics"],
    })

    result = normalize_categorical_columns(data)

    pd.testing.assert_frame_equal(result, expected)


def test_coerce_numeric_columns_converts_strings_and_fills_missing() -> None:
    """Verifies that values are correctly converted into numerical and that missing values are filled with the right default for each column."""

    data = pd.DataFrame({
        "quantity": ["2.0", None, 2.0],
        "unit_price": ["799.0", None, 2499.0],
        "discount": [None, "0.05", 0.2],
    })

    expected = pd.DataFrame({
            "quantity": [2.0, 1.0, 2.0],
            "unit_price": [799.0, 1649.0, 2499.0],
            "discount": [0.0, 0.05, 0.2],
        })

    result = coerce_numeric_columns(data)

    pd.testing.assert_frame_equal(result, expected)


def test_coerce_numeric_columns_invalid_and_negative_values() -> None:
    """Verifies that negative values are handled as invalid and filled with the right default for each column."""

    data = pd.DataFrame({
            "quantity": ["two", -1.0, 2.0],
            "unit_price": ["empty", -499.0, 2499.0],
            "discount": ["NOLL", 0.05, -0.2],
        })
    
    expected = pd.DataFrame({
            "quantity": [1.0, 1.0, 2.0],
            "unit_price": [2499.0, 2499.0, 2499.0],
            "discount": [0.0, 0.05, 0.0],
        })
    
    result = coerce_numeric_columns(data)

    pd.testing.assert_frame_equal(result, expected)


def test_convert_returned_to_boolean_recognizes_variants() -> None:
    """Verifies that known true values, casing, whitespaces and missing values are correctly converted into boolean values."""

    data = pd.DataFrame({
        "returned": ["  true", None, "yes", "false", "FAlse", "1", "JA"]
    })

    expected = pd.DataFrame({
        "returned": [True, False, True, False, False, True, True]
    })

    result = convert_returned_to_boolean(data)

    pd.testing.assert_frame_equal(result, expected)


def test_clean_order_data_valid_input_returns_cleaned_data() -> None:
    """Verifies that the cleaning pipeline works as expected taking in raw data, cleaning it and returning a corrected dataframe."""

    data = pd.DataFrame({
        "order_id": ["O0001", "O0002", "O0003"],
        "order_date": ["2026-01-04", "2026-03-17", "2026-03-13"],
        "customer_id": ["C018", "C028", "C013"],
        "region": ["South  ", "NORTH", " West"],
        "product_category": ["ELECTRONICS", "Electronics  ", "Electronics"],
        "quantity": [None, 1.0, 2.0],
        "unit_price": ["799.0", None, 2499.0],
        "discount": [None, 0.05, 0.2],
        "returned": ["YES", None, " false"],
    })

    expected = pd.DataFrame({
        "order_id": ["O0001", "O0002", "O0003"],
        "order_date": ["2026-01-04", "2026-03-17", "2026-03-13"],
        "customer_id": ["C018", "C028", "C013"],
        "region": ["South", "North", "West"],
        "product_category": ["Electronics", "Electronics", "Electronics"],
        "quantity": [1.0, 1.0, 2.0],
        "unit_price": [799.0, 1649.0, 2499.0],
        "discount": [0.0, 0.05, 0.2],
        "returned": [True, False, False],
    })

    result = clean_order_data(data)

    pd.testing.assert_frame_equal(result, expected)


def test_clean_order_data_empty_dataframe_raises_valueerror() -> None:
    """Verifies that a ValueError is raised in case the dataframe doesn't contain any rows."""

    data = pd.DataFrame({
        "order_id": [],
        "order_date": [],
        "customer_id": [],
        "region": [],
        "product_category": [],
        "quantity": [],
        "unit_price": [],
        "discount": [],
        "returned": [],
    })

    with pytest.raises(
        ValueError,
        match="Empty data: there are no rows to clean"
    ): clean_order_data(data)



def test_clean_order_data_does_not_mutate_input() -> None:
    """Verifies that the cleaning pipeline does not mutate the original dataframe."""

    data = pd.DataFrame({
        "order_id": ["O0001", "O0002", "O0003"],
        "order_date": ["2026-01-04", "2026-03-17", "2026-03-13"],
        "customer_id": ["C018", "C028", "C013"],
        "region": ["South  ", "NORTH", " West"],
        "product_category": ["ELECTRONICS", "Electronics  ", "Electronics"],
        "quantity": [None, 1.0, 2.0],
        "unit_price": ["799.0", None, 2499.0],
        "discount": [None, 0.05, 0.2],
        "returned": ["YES", None, " false"],
    })

    original = data.copy()

    result = clean_order_data(data)

    pd.testing.assert_frame_equal(data, original)