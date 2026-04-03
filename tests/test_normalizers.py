from src.normalizers import clean_amount, normalize_month


def test_normalize_month_variants():
    assert normalize_month("2026-01") == 1
    assert normalize_month("2026/01") == 1
    assert normalize_month("2026-1") == 1
    assert normalize_month("1") == 1
    assert normalize_month("01") == 1
    assert normalize_month("1月") == 1
    assert normalize_month("13") is None


def test_clean_amount_variants():
    amount, invalid, empty = clean_amount("¥1,234.50")
    assert amount == 1234.50
    assert not invalid
    assert not empty

    amount, invalid, empty = clean_amount("")
    assert amount == 0.0
    assert not invalid
    assert empty

    amount, invalid, empty = clean_amount("bad")
    assert amount == 0.0
    assert invalid
    assert not empty
