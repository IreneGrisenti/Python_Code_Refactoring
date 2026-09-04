"""Definierar konfigurationen för rapportgenereringen."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReportConfig:
    """Sökvägar för att skapa en rapport."""
    input_path: Path = Path("data/orders.csv")
    output_path: Path = Path("output_after_refactoring")