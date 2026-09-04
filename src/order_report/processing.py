"""Ansvarar för att transformera och aggregera order-datan till rapporter."""

import pandas as pd
import logging


logger = logging.getLogger(__name__)


def add_calculated_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Beräknar ordervärde och rabatterat värde och returnerar det som df."""

    logger.debug("Beräknar order_value och discounted_value för %d rader.", len(data))

    copied_data = data.copy()

    copied_data["order_value"] = (copied_data["quantity"] * copied_data["unit_price"])
    copied_data["discounted_value"] = (copied_data["order_value"] * (1 - copied_data["discount"]))

    return copied_data


def create_order_overview(data: pd.DataFrame) -> pd.DataFrame:
    """Tar emot en dataframe som redan inkluderar order_value och discounted_value, och returnerar en översikt."""

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
    """Delad aggregeringslogik: order count, total sales och returns per group_col"""

    return data.groupby(group_col, as_index=False).agg(
        order_count=("order_id", "nunique"),
        total_sales=("discounted_value", "sum"),
        returns=("returned", "sum")
    )


def create_sales_report(data: pd.DataFrame, group_col: str, sort_col: str, ascending: bool = False) -> pd.DataFrame:
    """Grupperar datan på group_col och beräknar antal ordrar, total försäljning, returer och returandel."""

    logger.info("Skapar sales-rapport grupperad på '%s'.", group_col)

    sales_result = _compute_group_metrics(data, group_col)

    sales_result["total_sales"] = sales_result["total_sales"].round(2)

    sales_result["return_rate"] = (sales_result["returns"] / sales_result["order_count"]).round(3)

    sales_result = sales_result.sort_values(sort_col, ascending=ascending).reset_index(drop=True)

    return sales_result


def create_returns_report(data: pd.DataFrame, group_col: str, sort_col: str, ascending: bool = False) -> pd.DataFrame:
    """Grupperar datan på group_col och beräknar antal ordrar, returer och returandel."""

    logger.info("Skapar return-rapport grupperad på '%s'.", group_col)

    returns_result = _compute_group_metrics(data, group_col)

    returns_result["return_rate"] = (returns_result["returns"] / returns_result["order_count"]).round(3)

    returns_result = returns_result[[group_col, "order_count", "returns", "return_rate"]]
    returns_result = returns_result.sort_values(sort_col, ascending=ascending).reset_index(drop=True)

    return returns_result
