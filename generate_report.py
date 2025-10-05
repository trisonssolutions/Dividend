import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
from fetch_data import (
    get_stock_dividends,
    get_previous_close,
    get_latest_eps,
    get_treasury_data,
)

def generate_report():
    """
    Fetches financial data, calculates key metrics, and generates a report
    with tables and a visualization.
    """
    # --- Data Collection ---
    common_stock_ticker = "MSFT"
    stock_dividends = get_stock_dividends(common_stock_ticker)
    stock_price = get_previous_close(common_stock_ticker)
    stock_eps = get_latest_eps(common_stock_ticker)
    treasury_data = get_treasury_data()

    # --- Common Stock Table ---
    print("--- Dividend Analysis: Common Stock ---")
    if stock_dividends and stock_price is not None and stock_eps is not None:
        latest_dividend = stock_dividends[0]
        dividend_per_share = latest_dividend['cash_amount']
        frequency = latest_dividend.get('frequency', 4)
        annual_dividend = dividend_per_share * frequency

        forward_yield = (annual_dividend / stock_price) * 100 if stock_price else 0
        payout_ratio = (dividend_per_share / stock_eps) * 100 if stock_eps and stock_eps != 0 else float('inf')

        stock_table_data = [
            ["Ticker", common_stock_ticker],
            ["Dividend per Share (Latest)", f"${dividend_per_share:.2f}"],
            ["Forward Dividend Yield (%)", f"{forward_yield:.2f}"],
            ["Dividend Payout Ratio (Quarterly, %)", f"{payout_ratio:.2f}"],
        ]
        print(tabulate(stock_table_data, headers=["Metric", "Value"], tablefmt="grid"))
    else:
        print("Could not retrieve complete data for common stock.")

    # --- Fixed Income Table & Visualization Data ---
    print("\n--- Interest Rate Analysis: Fixed Income ---")
    yield_data = {}
    if forward_yield:
        yield_data[common_stock_ticker] = forward_yield

    if treasury_data:
        df_treasury = pd.DataFrame(treasury_data)

        # T.I.P.S.
        tips_filter = "Inflation"
        tips_data = df_treasury[df_treasury['security_desc'].str.contains(tips_filter)].copy()
        tips_data['avg_interest_rate_amt'] = pd.to_numeric(tips_data['avg_interest_rate_amt'])
        latest_tips = tips_data.loc[tips_data['avg_interest_rate_amt'].idxmax()] if not tips_data.empty else None

        # Treasuries
        treasuries_filter = "Treasury Notes" # Focusing on a specific treasury type for comparison
        treasuries_data = df_treasury[df_treasury['security_desc'] == treasuries_filter].copy()
        treasuries_data['avg_interest_rate_amt'] = pd.to_numeric(treasuries_data['avg_interest_rate_amt'])
        latest_treasury_note = treasuries_data.iloc[0] if not treasuries_data.empty else None

        fixed_income_table = []
        if latest_tips is not None:
            fixed_income_table.append(["T.I.P.S.", f"{latest_tips['avg_interest_rate_amt']:.2f}%"])
            yield_data['T.I.P.S.'] = latest_tips['avg_interest_rate_amt']
        if latest_treasury_note is not None:
            fixed_income_table.append(["U.S. Treasury Note", f"{latest_treasury_note['avg_interest_rate_amt']:.2f}%"])
            yield_data['U.S. Treasury Note'] = latest_treasury_note['avg_interest_rate_amt']

        print(tabulate(fixed_income_table, headers=["Asset Class", "Latest Average Interest Rate"], tablefmt="grid"))

    else:
        print("Could not retrieve Treasury data.")

    # --- Visualization ---
    if yield_data:
        names = list(yield_data.keys())
        values = list(yield_data.values())

        plt.figure(figsize=(10, 6))
        bars = plt.bar(names, values, color=['skyblue', 'lightgreen', 'salmon'])
        plt.ylabel('Yield / Interest Rate (%)')
        plt.title('Yield Comparison: Stock vs. Fixed Income')
        plt.xticks(rotation=0)

        # Add values on top of bars
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2f}%', va='bottom', ha='center')

        plt.tight_layout()
        plt.savefig('yield_comparison.png')
        print("\nGenerated yield comparison chart: yield_comparison.png")
    else:
        print("\nNot enough data to generate a comparison chart.")

if __name__ == "__main__":
    generate_report()