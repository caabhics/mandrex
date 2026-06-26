from pathlib import Path
from typing import Dict, Optional

import pandas as pd


def load_financials(path: Path, sheet_name: Optional[str] = None) -> pd.DataFrame:
    """Load the first worksheet or a named worksheet from an Excel file."""
    sheet = sheet_name if sheet_name else 0
    df = pd.read_excel(path, sheet_name=sheet)
    df.columns = df.columns.map(str).str.strip()
    return df


def _get_value(row: pd.Series, keys: list[str]) -> Optional[float]:
    for key in keys:
        if key in row.index:
            value = row[key]
            try:
                return float(value)
            except (TypeError, ValueError):
                continue
    return None


def compute_financial_ratios(df: pd.DataFrame, year_row: int = -1) -> Dict[str, Optional[float]]:
    """Compute a small set of key financial ratios from the chosen row."""
    row = df.iloc[year_row]

    assets = _get_value(row, ["Total Assets", "Assets"])
    current_assets = _get_value(row, ["Current Assets", "Current asset", "Current assets"])
    current_liabilities = _get_value(row, ["Current Liabilities", "Current liability", "Current liabilities"])
    total_liabilities = _get_value(row, ["Total Liabilities", "Liabilities"])
    equity = _get_value(row, ["Total Equity", "Equity", "Shareholders' Equity", "Shareholders Equity"])
    net_income = _get_value(row, ["Net Income", "Net income", "Net Profit", "Profit"])
    revenue = _get_value(row, ["Revenue", "Sales", "Total Revenue"])
    cash = _get_value(row, ["Cash", "Cash and Cash Equivalents", "Cash and equivalents"])
    short_term_debt = _get_value(row, ["Short-term Debt", "Current Debt", "Current portion of debt"])
    ebit = _get_value(row, ["EBIT", "Operating Income", "Operating income"])
    interest_expense = _get_value(row, ["Interest Expense", "Interest expense", "Finance Costs"])

    ratios = {
        "Current Ratio": None,
        "Quick Ratio": None,
        "Debt to Equity": None,
        "Return on Equity": None,
        "Net Profit Margin": None,
        "Asset Turnover": None,
        "Cash Ratio": None,
        "Interest Coverage": None,
    }

    if current_assets is not None and current_liabilities:
        ratios["Current Ratio"] = current_assets / current_liabilities

    if cash is not None and current_liabilities:
        ratios["Quick Ratio"] = (cash) / current_liabilities

    if total_liabilities is not None and equity:
        ratios["Debt to Equity"] = total_liabilities / equity

    if net_income is not None and equity:
        ratios["Return on Equity"] = net_income / equity

    if net_income is not None and revenue:
        ratios["Net Profit Margin"] = net_income / revenue

    if revenue is not None and assets:
        ratios["Asset Turnover"] = revenue / assets

    if cash is not None and current_liabilities:
        ratios["Cash Ratio"] = cash / current_liabilities

    if ebit is not None and interest_expense:
        ratios["Interest Coverage"] = ebit / abs(interest_expense) if interest_expense != 0 else None

    return ratios


def format_ratio_table(ratios: Dict[str, Optional[float]]) -> str:
    lines = ["Financial ratios computed from the selected row:", ""]
    for label, value in ratios.items():
        if value is None:
            text = "N/A"
        else:
            text = f"{value:.2f}"
        lines.append(f"- {label}: {text}")
    lines.append("")
    lines.append("Tip: supply a different row with --year-row or name the sheet with --sheet.")
    return "\n".join(lines)
