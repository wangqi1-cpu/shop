from __future__ import annotations

INPUT_TABLES = [
    "sales_orders",
    "income_statement",
    "royalty_details",
    "cost_details",
    "operation_expenses",
    "platform_fees",
]

REQUIRED_COLUMNS = {
    "sales_orders": [
        "order_id",
        "order_date",
        "settlement_month",
        "channel",
        "product_name",
        "sku",
        "qty",
        "gross_sales_amount",
        "refund_amount",
        "net_sales_amount",
    ],
    "income_statement": [
        "txn_id",
        "received_date",
        "settlement_month",
        "income_type",
        "counterparty",
        "amount",
    ],
    "royalty_details": ["settlement_month", "ip_name", "royalty_amount"],
    "cost_details": ["cost_id", "settlement_month", "cost_type", "amount"],
    "operation_expenses": ["expense_id", "settlement_month", "expense_type", "amount"],
    "platform_fees": ["fee_id", "settlement_month", "fee_type", "platform", "amount"],
}

PRIMARY_KEYS = {
    "sales_orders": "order_id",
    "income_statement": "txn_id",
    "cost_details": "cost_id",
    "operation_expenses": "expense_id",
    "platform_fees": "fee_id",
}

ENUM_ALLOWED = {
    "income_type": {"渠道分销", "IP返采"},
    "ip_name": {
        "战双",
        "ES",
        "元气骑士",
        "雷亚",
        "少女的王座",
        "掌门太忙",
        "纸嫁衣",
        "剑网三",
        "风起长安",
        "灵猫传",
        "恋与制作人",
        "绘旅人",
        "phigros",
    },
    "cost_type": {"product_cost", "warehouse_cost", "shipping_cost"},
    "expense_type": {
        "customer_service_base_fee",
        "customer_service_bonus",
        "store_operation_base_fee",
        "store_misc_software_fee",
        "store_operation_bonus",
    },
    "fee_type": {"ad_spend", "platform_commission_fee"},
}

SHEET_ROW_MAPPING = {
    "ecom_gross_sales": 2,
    "channel_distribution_income": 3,
    "ip_buyback_income": 4,
    "ecom_net_sales_after_refund": 5,
    "royalty_pgr_10": 8,
    "royalty_es_12": 9,
    "royalty_soul_knight_13": 10,
    "royalty_rayark_20": 11,
    "royalty_queen_15": 12,
    "royalty_zhangmen_15": 13,
    "royalty_paper_doll_15": 14,
    "royalty_jx3_10": 15,
    "royalty_fqca_12": 16,
    "royalty_lingmao_15": 17,
    "royalty_mrlove_15": 18,
    "royalty_foralltime_10": 19,
    "royalty_phigros_10": 20,
    "product_cost": 23,
    "warehouse_cost": 25,
    "shipping_cost": 26,
    "customer_service_base_fee": 28,
    "customer_service_bonus": 29,
    "store_operation_base_fee": 30,
    "store_misc_software_fee": 31,
    "store_operation_bonus": 32,
    "ad_spend": 35,
    "platform_commission_fee": 36,
}

IP_METRIC_NAME = {
    "战双": "royalty_pgr_10",
    "ES": "royalty_es_12",
    "元气骑士": "royalty_soul_knight_13",
    "雷亚": "royalty_rayark_20",
    "少女的王座": "royalty_queen_15",
    "掌门太忙": "royalty_zhangmen_15",
    "纸嫁衣": "royalty_paper_doll_15",
    "剑网三": "royalty_jx3_10",
    "风起长安": "royalty_fqca_12",
    "灵猫传": "royalty_lingmao_15",
    "恋与制作人": "royalty_mrlove_15",
    "绘旅人": "royalty_foralltime_10",
    "phigros": "royalty_phigros_10",
}

MONTH_TO_COLUMN = {month: chr(ord("C") + month) for month in range(1, 13)}

AMOUNT_COLUMNS = {
    "sales_orders": ["gross_sales_amount", "refund_amount", "net_sales_amount"],
    "income_statement": ["amount"],
    "royalty_details": ["royalty_amount"],
    "cost_details": ["amount"],
    "operation_expenses": ["amount"],
    "platform_fees": ["amount"],
}

ENUM_COLUMN_BY_TABLE = {
    "income_statement": ["income_type"],
    "royalty_details": ["ip_name"],
    "cost_details": ["cost_type"],
    "operation_expenses": ["expense_type"],
    "platform_fees": ["fee_type"],
}
