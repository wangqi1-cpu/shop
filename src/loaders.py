from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from config.mappings import INPUT_TABLES
from src.models import ValidationReport

logger = logging.getLogger(__name__)


def _find_table_file(input_dir: Path, table_name: str) -> Path | None:
    for ext in ("xlsx", "csv"):
        path = input_dir / f"{table_name}.{ext}"
        if path.exists():
            return path
    return None


def _empty_df() -> pd.DataFrame:
    return pd.DataFrame()


def load_input_tables(input_dir: str | Path, report: ValidationReport) -> dict[str, pd.DataFrame]:
    input_path = Path(input_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"Input dir not found: {input_dir}")

    tables: dict[str, pd.DataFrame] = {}
    for table_name in INPUT_TABLES:
        file_path = _find_table_file(input_path, table_name)
        if not file_path:
            logger.warning("Missing table file: %s", table_name)
            report.add(table_name, "missing_table", "table file missing, treated as empty", 1)
            tables[table_name] = _empty_df()
            continue

        if file_path.suffix.lower() == ".xlsx":
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)

        logger.info("Loaded table %s rows=%s", table_name, len(df))
        tables[table_name] = df

    return tables
