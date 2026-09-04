"""Kör order-rapportens pipeline."""

from order_report.config import ReportConfig
from order_report.logging_config import configure_logging
from order_report.pipeline import run_pipeline

def main() -> None:
    configure_logging()
    run_pipeline(ReportConfig())

if __name__ == "__main__":
    main()