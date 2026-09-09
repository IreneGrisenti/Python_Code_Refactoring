"""Runs the order report pipeline."""


import logging
from order_report.config import ReportConfig
from order_report.logging_config import configure_logging
from order_report.pipeline import run_pipeline


logger = logging.getLogger("order_report")


def main() -> int:

    configure_logging()

    try:
        run_pipeline(ReportConfig())
    except (ValueError, FileNotFoundError, KeyError) as error:
        logger.error("The pipeline was stopped: %s", error)
        return 1
    except Exception:
        logger.exception("An unexpected error stopped the pipeline")
        raise

    logger.info("Program completed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())