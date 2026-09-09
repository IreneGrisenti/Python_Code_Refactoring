"""Defines configurations for the report generation."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReportConfig:
    """Search paths to load or save a file."""
    input_path: Path = Path("data/orders.csv")
    output_path: Path = Path("output_after_refactoring")