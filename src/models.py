from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd


@dataclass
class ValidationIssue:
    table: str
    issue_type: str
    detail: str
    count: int = 1


@dataclass
class ValidationReport:
    issues: list[ValidationIssue] = field(default_factory=list)

    def add(self, table: str, issue_type: str, detail: str, count: int = 1) -> None:
        self.issues.append(ValidationIssue(table, issue_type, detail, count))

    def to_dataframe(self) -> pd.DataFrame:
        if not self.issues:
            return pd.DataFrame(columns=["table", "issue_type", "detail", "count"])
        return pd.DataFrame([i.__dict__ for i in self.issues])


@dataclass
class ProcessedTable:
    name: str
    df: pd.DataFrame


AggregatedResult = dict[int, dict[str, float]]
AnyDict = dict[str, Any]
