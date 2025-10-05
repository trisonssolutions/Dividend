import requests
import pandas as pd
import os

# Get API key from environment variable for security
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

def check_api_key():
    """Checks if the Polygon API key is set."""
    if not POLYGON_API_KEY:
        print("Error: POLYGON_API_KEY environment variable not set.")
        print("Please set the variable and try again.")
        return False
    return True

def get_stock_dividends(ticker):
    if not check_api_key(): return None
    url = f"https://api.polygon.io/v3/reference/dividends?ticker={ticker}&apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200 and response.json().get("results"):
        return response.json()["results"]
    return None

def get_previous_close(ticker):
    if not check_api_key(): return None
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200 and response.json().get("resultsCount", 0) > 0:
        return response.json()["results"][0].get("c")
    return None

def get_latest_eps(ticker):
    if not check_api_key(): return None
    url = f"https://api.polygon.io/vX/reference/financials?ticker={ticker}&limit=1&timeframe=quarterly&sort=filing_date&apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200 and response.json().get("results"):
        financials = response.json()["results"][0]
        income_statement = financials.get("financials", {}).get("income_statement", {})
        basic_eps = income_statement.get("basic_earnings_per_share", {})
        if "value" in basic_eps:
            return basic_eps["value"]
    # Suppressing debug output for cleaner execution
    # print(f"DEBUG: Could not fetch EPS for {ticker}. Status: {response.status_code}, Response: {response.text}")
    return None

def get_treasury_data():
    url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?sort=-record_date&page[number]=1&page[size]=100"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["data"]
    return None

if __name__ == "__main__":
    # This part is for direct execution testing and is not used by generate_report.py
    if not check_api_key():
        exit(1)

    print("--- Testing data fetching functions ---")

    # Test Common Stock
    common_stock_ticker = "MSFT"
    print(f"\nFetching data for {common_stock_ticker}...")
    dividends = get_stock_dividends(common_stock_ticker)
    price = get_previous_close(common_stock_ticker)
    eps = get_latest_eps(common_stock_ticker)
    print(f"  Dividends: {'OK' if dividends else 'Failed'}")
    print(f"  Price: {'OK' if price else 'Failed'}")
    print(f"  EPS: {'OK' if eps else 'Failed'}")

    # Test Treasury Data
    print("\nFetching Treasury data...")
    treasury = get_treasury_data()
    print(f"  Treasury Data: {'OK' if treasury else 'Failed'}")
    if treasury:
        df_treasury = pd.DataFrame(treasury)
        print("  Sample Treasury Data:")
        print(df_treasury.head(2))