"""Mandrex financial evaluator package."""

from .analysis import compute_financial_ratios, format_ratio_table, load_financials

__all__ = ["load_financials", "compute_financial_ratios", "format_ratio_table"]
