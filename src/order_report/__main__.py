"""Kör order-rapportens pipeline."""

from config import ReportConfig
from logging_config import configure_logging
from pipeline import run_pipeline

def main() -> None:
    configure_logging()
    run_pipeline(ReportConfig())

if __name__ == "__main__":
    main()