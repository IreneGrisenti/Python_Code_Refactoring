"""
Tests for processing.py.

Checks that processing.py functions perform corretly with the following tests:
1. add_calculated_columns computes order_value and discounted_value correctly.
2. add_calculated_columns verifies the columns are correctly calculated at edge values for quantity and discount.
3. create_order_overview aggregates total_sales, order_count and returns correctly.
4. create_order_overview raises ValueError when a required column is missing from the input data.
5. create_sales_report groups by product_category and computes order_count, total_sales and return_rate correctly.
6. create_sales_report groups by region and computes order_count, total_sales and return_rate correctly.
7. create_returns_report groups by product_category and computes order_count, returns and return_rate correctly.
"""


import pandas as pd
import pytest
from order_report.processing import (
    add_calculated_columns,
    create_order_overview,
    create_sales_report,
    create_returns_report
)


def test_add_calculated_columns_normal() -> None:
    """Verifies that order_value and discounted_value are calculated correctly from quantity, unit_price and discount."""

    data = pd.DataFrame({
        "quantity": [1.0, 1.0, 2.0],
        "unit_price": [100.0, 100.0, 200.0],
        "discount": [0.0, 0.05, 0.2],
    })

    result = add_calculated_columns(data)

    assert result["order_value"].tolist() == pytest.approx([100.0, 100.0, 400.0])
    assert result["discounted_value"].tolist() == pytest.approx([100.0, 95.0, 320.0])


def test_add_calculated_columns_boundary_values() -> None:
    """Verifies order_value and discount_value at zero quantity, 0% discount and 100% discount."""

    data = pd.DataFrame({
        "quantity": [0.0, 2.0, 3.0],
        "unit_price": [100.0, 50.0, 10.0],
        "discount": [0.0, 1.0, 0.0],
    })

    result = add_calculated_columns(data)

    assert result["order_value"].tolist() == pytest.approx([0.0, 100.0, 30.0])
    assert result["discounted_value"].tolist() == pytest.approx([0.0, 0.0, 30.0])


def test_create_order_overview_normal() -> None:
    """Verifies that total_sales, order_count and return_count are aggregated correctly."""

    data = pd.DataFrame({
            "order_id": ["O0001", "O0002", "O0003"],
            "quantity": [1.0, 1.0, 2.0],
            "unit_price": [100.0, 100.0, 200.0],
            "discount": [0.0, 0.05, 0.2],
            "returned": [True, False, False],
            })

    data_with_calculated_cols = add_calculated_columns(data)
    result = create_order_overview(data_with_calculated_cols)

    expected = pd.DataFrame({
        "metric": ["total_sales", "order_count", "return_count"],
        "value": [ 515.0, 3, 1]
        })

    pd.testing.assert_frame_equal(expected, result)


def test_create_order_overview_missing_col() -> None:
    """Verifies that create_order_overview raises ValueError when a required column is missing from the input data."""

    data = pd.DataFrame({
                "order_id": ["O0001", "O0002", "O0003"],
                "quantity": [1.0, 1.0, 2.0],
                "unit_price": [100.0, 100.0, 200.0],
                "discount": [0.0, 0.05, 0.2],
                "returned": [True, False, False],
                })

    with pytest.raises(
        ValueError,
        match="Missing columns: discounted_value"
    ): create_order_overview(data)


def test_create_sales_report_by_category() -> None:
    """Verifies that create_sales_report correctly computes order_count, total_sales and return_rate when grouped by product_category."""

    data = pd.DataFrame({
        "order_id": ["O0001", "O0002", "O0003", "O0004"],
        "order_date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"],
        "customer_id": ["C001", "C002", "C003", "C004"],
        "region": ["North", "North", "South", "South"],
        "product_category": ["Electronics", "Electronics", "Clothing", "Clothing"],
        "quantity": [1.0, 1.0, 2.0, 1.0],
        "unit_price": [100.0, 100.0, 50.0, 50.0],
        "discount": [0.0, 0.5, 0.0, 0.0],
        "returned": [False, True, False, True],
    })

    data_with_calculated_cols = add_calculated_columns(data)
    result = create_sales_report(
        data_with_calculated_cols, 
        group_col="product_category", 
        sort_col="total_sales",
        ascending=True,
    )

    expected = pd.DataFrame({
        "product_category": ["Clothing", "Electronics"],
        "order_count": [2, 2],
        "total_sales": [150.0, 150.0],
        "returns": [1, 1],
        "return_rate": [0.5, 0.5],
    })

    pd.testing.assert_frame_equal(expected, result)


def test_create_sales_report_group_by_region() -> None:
    """Verifies that create_sales_report correctly computes order_count, total_sales and return_rate when grouped by region."""

    data = pd.DataFrame({
        "order_id": ["O0001", "O0002", "O0003", "O0004"],
        "order_date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"],
        "customer_id": ["C001", "C002", "C003", "C004"],
        "region": ["North", "North", "South", "South"],
        "product_category": ["Electronics", "Electronics", "Clothing", "Clothing"],
        "quantity": [1.0, 1.0, 2.0, 1.0],
        "unit_price": [100.0, 100.0, 50.0, 50.0],
        "discount": [0.0, 0.5, 0.0, 0.0],
        "returned": [False, True, False, True],
    })

    data_with_calculated_cols = add_calculated_columns(data)
    result = create_sales_report(
        data_with_calculated_cols, 
        group_col="region", 
        sort_col="total_sales",
        ascending=True,
    )

    expected = pd.DataFrame({
        "region": ["North", "South"],
        "order_count": [2, 2],
        "total_sales": [150.0, 150.0],
        "returns": [1, 1],
        "return_rate": [0.5, 0.5],
    })

    pd.testing.assert_frame_equal(expected, result)


def test_create_returns_report_normal() -> None:
    """Verifies that create_returns_report correctly computes order_count, returns and return_rate per group."""
    
    data = pd.DataFrame({
        "order_id": ["O0001", "O0002", "O0003", "O0004"],
        "order_date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"],
        "customer_id": ["C001", "C002", "C003", "C004"],
        "region": ["North", "North", "South", "South"],
        "product_category": ["Electronics", "Electronics", "Clothing", "Clothing"],
        "quantity": [1.0, 1.0, 2.0, 1.0],
        "unit_price": [100.0, 100.0, 50.0, 50.0],
        "discount": [0.0, 0.5, 0.0, 0.0],
        "returned": [False, False, False, True],
    })

    data_with_calculated_cols = add_calculated_columns(data)
    result = create_returns_report(
        data_with_calculated_cols, 
        group_col="product_category", 
        sort_col="return_rate",
        ascending=True,
    )

    expected = pd.DataFrame({
            "product_category": ["Electronics", "Clothing"],
            "order_count": [2, 2],
            "returns": [0, 1],
            "return_rate": [0.0, 0.5],
        })

    pd.testing.assert_frame_equal(expected, result)