# Financial Data Analysis Tool

This project fetches, analyzes, and visualizes dividend and interest rate data for various financial assets, including common stocks, T.I.P.S., and U.S. Treasuries.

## Features

-   Fetches dividend data for common stocks from Polygon.io.
-   Calculates key metrics: Dividend Per Share, Forward Dividend Yield, and Dividend Payout Ratio.
-   Fetches interest rate data for U.S. Treasuries and T.I.P.S. from the U.S. Treasury Fiscal Data API.
-   Presents the findings in clear, command-line-based tables.
-   Generates a bar chart to visually compare the yields of the different asset classes.

## Prerequisites

-   Python 3
-   A Polygon.io API key

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file should be created for a more robust setup, but for now, you can install manually as per the next step if needed.)*

    Alternatively, install packages individually:
    ```bash
    pip install requests pandas matplotlib tabulate
    ```

3.  **Set up the Polygon.io API Key:**
    This tool requires an API key from Polygon.io. You must set it as an environment variable.

    **On macOS/Linux:**
    ```bash
    export POLYGON_API_KEY="YOUR_API_KEY_HERE"
    ```

    **On Windows (Command Prompt):**
    ```bash
    set POLYGON_API_KEY="YOUR_API_KEY_HERE"
    ```

    **On Windows (PowerShell):**
    ```bash
    $env:POLYGON_API_KEY="YOUR_API_KEY_HERE"
    ```

    Replace `"YOUR_API_KEY_HERE"` with your actual Polygon.io API key.

## Usage

To generate the report, run the `generate_report.py` script from your terminal:

```bash
python3 generate_report.py
```

The script will output:
-   A table with dividend analysis for a common stock (e.g., MSFT).
-   A table with the latest average interest rates for fixed-income assets.
-   A PNG image file named `yield_comparison.png` in the root directory, containing a bar chart of the yield comparison.

## Note on Data Availability

-   **Preferred Stocks:** Data for specific preferred stocks is often limited on free-tier APIs like Polygon.io. As such, this analysis has been omitted from the final report.
-   **Other Fixed Income:** Data for municipal and convertible bonds was not readily available through free, public APIs and is not included. The report focuses on assets for which reliable data could be sourced.