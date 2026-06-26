from pathlib import Path
import argparse

from mandrex.analysis import load_financials, compute_financial_ratios, format_ratio_table


def parse_args():
    parser = argparse.ArgumentParser(
        description="Mandrex financial evaluator: computes key ratios from a financial Excel file."
    )
    parser.add_argument(
        "file",
        nargs="?",
        default="examples/financials.xlsx",
        help="Path to the financial Excel file (default: examples/financials.xlsx)",
    )
    parser.add_argument(
        "--sheet",
        help="Optional sheet name to read from the Excel file. If omitted, the first sheet is used.",
    )
    parser.add_argument(
        "--year-row",
        type=int,
        default=-1,
        help="Row index to compute ratios from, starting at 0. Default is the last row.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    path = Path(args.file)

    if not path.exists():
        raise FileNotFoundError(
            f"Excel file not found: {path}. Place your file in examples/ or pass a valid path."
        )

    df = load_financials(path, args.sheet)
    ratios = compute_financial_ratios(df, year_row=args.year_row)
    print(format_ratio_table(ratios))


if __name__ == "__main__":
    main()
