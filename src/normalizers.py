from __future__ import annotations

import re
from typing import Any

import pandas as pd


def normalize_month(value: Any) -> int | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    if not text:
        return None

    text = text.replace("月", "")
    text = text.replace("/", "-")
    match = re.search(r"(\d{4})-(\d{1,2})$", text)
    if match:
        month = int(match.group(2))
        return month if 1 <= month <= 12 else None

    if re.fullmatch(r"\d{1,2}", text):
        month = int(text)
        return month if 1 <= month <= 12 else None

    return None


def clean_amount(value: Any) -> tuple[float, bool, bool]:
    """returns (amount, is_invalid, was_empty_as_zero)."""
    if pd.isna(value) or str(value).strip() == "":
        return 0.0, False, True

    text = str(value).strip()
    text = text.replace(",", "").replace("¥", "").replace("￥", "").replace(" ", "")
    try:
        return float(text), False, False
    except ValueError:
        return 0.0, True, False


def normalize_text_enum(value: Any) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()
