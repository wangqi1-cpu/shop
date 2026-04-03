from __future__ import annotations

import argparse
import logging
from pathlib import Path

from src.aggregators import aggregate_monthly
from src.excel_writer import write_back_to_excel
from src.loaders import load_input_tables
from src.models import ValidationReport
from src.utils import setup_logging
from src.validators import validate_and_normalize_tables

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="电商店铺月度利润自动回填工具")
    parser.add_argument("--template", required=True, help="利润总表模板路径")
    parser.add_argument("--input-dir", required=True, help="输入目录")
    parser.add_argument("--year", required=True, type=int, help="目标年份，如 2026")
    parser.add_argument("--output", required=True, help="输出Excel路径")
    return parser.parse_args()


def main() -> None:
    setup_logging()
    args = parse_args()

    report = ValidationReport()
    logger.info("Start processing year=%s", args.year)

    tables = load_input_tables(args.input_dir, report)
    normalized_tables = validate_and_normalize_tables(tables, report)
    aggregated = aggregate_monthly(normalized_tables, args.year)

    write_back_to_excel(
        template_path=args.template,
        output_path=args.output,
        year=args.year,
        aggregated=aggregated,
        report=report,
    )

    logger.info("Done. Output saved to %s", Path(args.output).resolve())


if __name__ == "__main__":
    main()
