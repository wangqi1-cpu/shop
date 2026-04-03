from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    main_sheet_name: str = "2026"
    description_sheet_name: str = "数据释意"
    validation_sheet_name: str = "validation_report"
    tax_rate_income: float = 0.13
    ratio_default_zero: bool = True


SETTINGS = Settings()
