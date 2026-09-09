"""Responsible for compiling and saving reports."""

import pandas as pd
import logging
from order_report.config import ReportConfig
from order_report.file_handler import load_data, save_report
from order_report.validation import validate_order_data
from order_report.processing import add_calculated_columns, create_order_overview, create_sales_report, create_returns_report


logger = logging.getLogger(__name__)
 

def run_pipeline(config: ReportConfig) -> dict[str, pd.DataFrame]:
    """Runs the entire pipeline from reading a file to saving reports."""

    logger.info("Starting to load data")
    data = load_data(config.input_path)
    logger.info("Data loaded")

    logger.info("Starting validation process")
    validated_data = validate_order_data(data)
    logger.info("Validation completed")

    logger.info("Starting processing data")
    enriched_data = add_calculated_columns(validated_data)

    reports = {
        "overview": create_order_overview(enriched_data),
        "sales_by_category": create_sales_report(enriched_data, group_col="product_category", sort_col="total_sales"),
        "sales_by_region": create_sales_report(enriched_data, group_col="region", sort_col="total_sales"),
        "returns_by_category": create_returns_report(enriched_data, group_col="product_category", sort_col="return_rate")
    }
    logger.info("Processing completed")

    logger.info("Starting to save reports")
    for report_key, report in reports.items():
        save_report(report, config.output_path, report_key)
    logger.info("Pipeline completed, %d reports saved in %s", len(reports), config.output_path)

    return reports