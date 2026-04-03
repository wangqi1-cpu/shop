import pandas as pd

from src.aggregators import aggregate_monthly
from src.models import ValidationReport
from src.validators import validate_and_normalize_tables


def test_enum_validation_and_aggregation():
    tables = {
        "sales_orders": pd.DataFrame(
            [{"order_id": "1", "order_date": "2026-01-01", "settlement_month": "1", "channel": "a", "product_name": "p", "sku": "s", "qty": 1, "gross_sales_amount": "100", "refund_amount": "0", "net_sales_amount": "90"}]
        ),
        "income_statement": pd.DataFrame(
            [
                {"txn_id": "t1", "received_date": "2026-01-01", "settlement_month": "1", "income_type": "渠道分销", "counterparty": "x", "amount": "10"},
                {"txn_id": "t2", "received_date": "2026-01-01", "settlement_month": "1", "income_type": "未知", "counterparty": "x", "amount": "10"},
            ]
        ),
        "royalty_details": pd.DataFrame([{"settlement_month": "1", "ip_name": "战双", "royalty_amount": "8"}]),
        "cost_details": pd.DataFrame([{"cost_id": "c1", "settlement_month": "1", "cost_type": "product_cost", "amount": "20"}]),
        "operation_expenses": pd.DataFrame([{"expense_id": "e1", "settlement_month": "1", "expense_type": "store_operation_bonus", "amount": "5"}]),
        "platform_fees": pd.DataFrame([{"fee_id": "f1", "settlement_month": "1", "fee_type": "ad_spend", "platform": "tb", "amount": "3"}]),
    }

    report = ValidationReport()
    normalized = validate_and_normalize_tables(tables, report)
    result = aggregate_monthly(normalized, 2026)

    assert result[1]["ecom_gross_sales"] == 100.0
    assert result[1]["ecom_net_sales_after_refund"] == 90.0
    assert result[1]["channel_distribution_income"] == 10.0
    assert result[1]["royalty_pgr_10"] == 8.0
    assert result[1]["product_cost"] == 20.0
    assert result[1]["store_operation_bonus"] == 5.0
    assert result[1]["ad_spend"] == 3.0

    df = report.to_dataframe()
    assert (df["issue_type"] == "unknown_enum").any()
