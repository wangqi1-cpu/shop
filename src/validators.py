from __future__ import annotations

from typing import Iterable

import pandas as pd

from config.mappings import (
    AMOUNT_COLUMNS,
    ENUM_ALLOWED,
    ENUM_COLUMN_BY_TABLE,
    PRIMARY_KEYS,
    REQUIRED_COLUMNS,
)
from src.models import ValidationReport
from src.normalizers import clean_amount, normalize_month, normalize_text_enum


def _validate_required_columns(table: str, df: pd.DataFrame, report: ValidationReport) -> None:
    missing = [c for c in REQUIRED_COLUMNS[table] if c not in df.columns]
    if missing:
        report.add(table, "missing_required_columns", ",".join(missing), len(missing))


def _validate_duplicates(table: str, df: pd.DataFrame, report: ValidationReport) -> None:
    pk = PRIMARY_KEYS.get(table)
    if not pk or pk not in df.columns or df.empty:
        return
    duplicated = df[pk].astype(str).duplicated(keep=False)
    count = int(duplicated.sum())
    if count:
        report.add(table, "duplicate_primary_key", pk, count)


def _normalize_month_column(table: str, df: pd.DataFrame, report: ValidationReport) -> pd.DataFrame:
    if "settlement_month" not in df.columns:
        return df
    normalized = df["settlement_month"].map(normalize_month)
    invalid_count = int(normalized.isna().sum())
    if invalid_count:
        report.add(table, "invalid_month", "settlement_month", invalid_count)
    df = df.copy()
    df["settlement_month"] = normalized
    return df


def _normalize_amounts(table: str, df: pd.DataFrame, report: ValidationReport) -> pd.DataFrame:
    amount_cols = [c for c in AMOUNT_COLUMNS.get(table, []) if c in df.columns]
    if not amount_cols:
        return df
    df = df.copy()
    for col in amount_cols:
        cleaned = df[col].map(clean_amount)
        df[col] = cleaned.map(lambda x: x[0])
        invalid_count = int(cleaned.map(lambda x: x[1]).sum())
        empty_count = int(cleaned.map(lambda x: x[2]).sum())
        if invalid_count:
            report.add(table, "invalid_amount", col, invalid_count)
        if empty_count:
            report.add(table, "empty_amount_filled_zero", col, empty_count)
    return df


def _validate_enums(table: str, df: pd.DataFrame, report: ValidationReport) -> pd.DataFrame:
    enum_cols = ENUM_COLUMN_BY_TABLE.get(table, [])
    if not enum_cols:
        return df
    df = df.copy()
    for col in enum_cols:
        if col not in df.columns:
            continue
        df[col] = df[col].map(normalize_text_enum)
        allowed = ENUM_ALLOWED[col]
        invalid = (~df[col].isin(allowed)) & (df[col] != "")
        invalid_count = int(invalid.sum())
        if invalid_count:
            values = sorted(set(df.loc[invalid, col].tolist()))
            report.add(table, "unknown_enum", f"{col}:{values}", invalid_count)
    return df


def _validate_missing_ip_mapping(df: pd.DataFrame, report: ValidationReport) -> None:
    if "ip_name" not in df.columns or df.empty:
        return
    unknown = (~df["ip_name"].isin(ENUM_ALLOWED["ip_name"])) & (df["ip_name"] != "")
    cnt = int(unknown.sum())
    if cnt:
        report.add("royalty_details", "missing_ip_mapping", "ip_name not mapped", cnt)


def validate_and_normalize_tables(
    tables: dict[str, pd.DataFrame], report: ValidationReport
) -> dict[str, pd.DataFrame]:
    processed: dict[str, pd.DataFrame] = {}
    for table, df in tables.items():
        if df.empty:
            processed[table] = df
            continue

        _validate_required_columns(table, df, report)
        _validate_duplicates(table, df, report)
        df = _normalize_month_column(table, df, report)
        df = _normalize_amounts(table, df, report)
        df = _validate_enums(table, df, report)
        if table == "royalty_details":
            _validate_missing_ip_mapping(df, report)

        processed[table] = df

    return processed
