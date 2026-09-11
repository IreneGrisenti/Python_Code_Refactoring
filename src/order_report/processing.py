"""Handles transforming and aggregating the order data into reports."""

import pandas as pd
import logging


logger = logging.getLogger(__name__)


def add_calculated_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Calculates order value and discounted value, and returns it as a df."""

    logger.debug("Calculating order_value and discounted_value for %d rows", len(data))

    copied_data = data.copy()

    copied_data["order_value"] = (copied_data["quantity"] * copied_data["unit_price"])
    copied_data["discounted_value"] = (copied_data["order_value"] * (1 - copied_data["discount"]))

    return copied_data


def _check_required_columns(data: pd.DataFrame, required_columns: set[str]) -> None:
    """Checks that all required columns are present in the input dataframe."""

    missing_columns = required_columns - set(data.columns)

    if missing_columns:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing_columns))}")


def create_order_overview(data: pd.DataFrame) -> pd.DataFrame:
    """Takes a dataframe that includes order_id, discounted_value and returned, and returns an overview."""

    logger.info("Creating orders overview")

    _check_required_columns(data, {"order_id", "discounted_value", "returned"})

    total_sales = round(data["discounted_value"].sum(), 2)

    number_of_orders = data["order_id"].nunique()

    number_of_returns = int(data["returned"].sum())

    order_overview = pd.DataFrame(
            {
                "metric": ["total_sales", "order_count", "return_count"],
                "value": [total_sales, number_of_orders, number_of_returns],
            }
        )

    return order_overview


def _compute_group_metrics(data: pd.DataFrame, group_col: str) -> pd.DataFrame:
    """Performs aggregation logic: order count, total sales, returns and return_rate per group_col."""

    result = data.groupby(group_col, as_index=False).agg(
        order_count=("order_id", "nunique"),
        total_sales=("discounted_value", "sum"),
        returns=("returned", "sum")
    )

    result["return_rate"] = (result["returns"] / result["order_count"]).round(3)

    return result


def create_sales_report(data: pd.DataFrame, group_col: str, sort_col: str, ascending: bool = False) -> pd.DataFrame:
    """Takes a dataframe that includes order_id, discounted_value, and creates a sales report by group_col."""

    logger.info("Creating sales report grouped by '%s'", group_col)

    _check_required_columns(data, {"order_id", "discounted_value", "returned"})
    
    sales_result = _compute_group_metrics(data, group_col)

    sales_result["total_sales"] = sales_result["total_sales"].round(2)

    sales_result = sales_result.sort_values(sort_col, ascending=ascending).reset_index(drop=True)

    return sales_result


def create_returns_report(data: pd.DataFrame, group_col: str, sort_col: str, ascending: bool = False) -> pd.DataFrame:
    """Takes a dataframe that includes order_id, discounted_value, and creates a returns report by group_col."""

    logger.info("Creating returns report grouped by '%s'", group_col)

    _check_required_columns(data, {"order_id", "discounted_value", "returned"})
    
    returns_result = _compute_group_metrics(data, group_col)

    returns_result = returns_result[[group_col, "order_count", "returns", "return_rate"]]
    returns_result = returns_result.sort_values(sort_col, ascending=ascending).reset_index(drop=True)

    return returns_result
