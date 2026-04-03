from __future__ import annotations

import pandas as pd

from config.mappings import IP_METRIC_NAME


def _monthly_metric_bucket() -> dict[int, dict[str, float]]:
    return {m: {} for m in range(1, 13)}


def _put(metrics: dict[int, dict[str, float]], month: int, key: str, value: float) -> None:
    metrics[month][key] = metrics[month].get(key, 0.0) + float(value)


def aggregate_monthly(tables: dict[str, pd.DataFrame], year: int) -> dict[int, dict[str, float]]:
    del year  # MVP phase: currently by month only, year can be used in future extension.
    metrics = _monthly_metric_bucket()

    sales = tables.get("sales_orders", pd.DataFrame())
    if not sales.empty and {"settlement_month", "gross_sales_amount", "net_sales_amount"}.issubset(sales.columns):
        for _, row in sales.dropna(subset=["settlement_month"]).iterrows():
            m = int(row["settlement_month"])
            if 1 <= m <= 12:
                _put(metrics, m, "ecom_gross_sales", row["gross_sales_amount"])
                _put(metrics, m, "ecom_net_sales_after_refund", row["net_sales_amount"])

    income = tables.get("income_statement", pd.DataFrame())
    if not income.empty and {"settlement_month", "income_type", "amount"}.issubset(income.columns):
        for _, row in income.dropna(subset=["settlement_month"]).iterrows():
            m = int(row["settlement_month"])
            if not (1 <= m <= 12):
                continue
            if row["income_type"] == "渠道分销":
                _put(metrics, m, "channel_distribution_income", row["amount"])
            elif row["income_type"] == "IP返采":
                _put(metrics, m, "ip_buyback_income", row["amount"])

    royalty = tables.get("royalty_details", pd.DataFrame())
    if not royalty.empty and {"settlement_month", "ip_name", "royalty_amount"}.issubset(royalty.columns):
        for _, row in royalty.dropna(subset=["settlement_month"]).iterrows():
            m = int(row["settlement_month"])
            if 1 <= m <= 12 and row["ip_name"] in IP_METRIC_NAME:
                _put(metrics, m, IP_METRIC_NAME[row["ip_name"]], row["royalty_amount"])

    cost = tables.get("cost_details", pd.DataFrame())
    if not cost.empty and {"settlement_month", "cost_type", "amount"}.issubset(cost.columns):
        for _, row in cost.dropna(subset=["settlement_month"]).iterrows():
            m = int(row["settlement_month"])
            if 1 <= m <= 12 and row["cost_type"] in {"product_cost", "warehouse_cost", "shipping_cost"}:
                _put(metrics, m, row["cost_type"], row["amount"])

    operation = tables.get("operation_expenses", pd.DataFrame())
    if not operation.empty and {"settlement_month", "expense_type", "amount"}.issubset(operation.columns):
        for _, row in operation.dropna(subset=["settlement_month"]).iterrows():
            m = int(row["settlement_month"])
            if 1 <= m <= 12:
                _put(metrics, m, row["expense_type"], row["amount"])

    fees = tables.get("platform_fees", pd.DataFrame())
    if not fees.empty and {"settlement_month", "fee_type", "amount"}.issubset(fees.columns):
        for _, row in fees.dropna(subset=["settlement_month"]).iterrows():
            m = int(row["settlement_month"])
            if 1 <= m <= 12:
                _put(metrics, m, row["fee_type"], row["amount"])

    return metrics
