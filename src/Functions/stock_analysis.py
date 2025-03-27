import yfinance as yf
import pandas as pd
from datetime import date, timedelta
from src.Brain.ask_gemini import generate_financial_insights

def fetch_financial_data(ticker):
    """Fetch financial statements, balance sheet, and cash flow."""
    company = yf.Ticker(ticker)
    return {
        "info": company.info,
        "income_stmt": company.financials,
        "balance_sheet": company.balance_sheet,
        "cash_flow": company.cashflow,
        "history": fetch_recent_history(company),
    }

def fetch_recent_history(company):
    """Fetch recent stock price history (last 5 days)."""
    end_date = date.today()
    start_date = end_date - timedelta(days=5)
    history = company.history(start=start_date.isoformat(), end=end_date.isoformat())
    
    # Selecting relevant columns from historical data
    return history[["Open", "High", "Low", "Close", "Volume"]]

def safe_get(df, key):
    """Safely extract data from DataFrame, return None if key is missing."""
    return df.loc[key].iloc[0] if key in df.index else None

def extract_key_metrics(ticker):
    """Extract key financial data and return as structured dictionary."""
    data = fetch_financial_data(ticker)
    info, income_stmt, balance_sheet, cash_flow = (
        data["info"],
        data["income_stmt"],
        data["balance_sheet"],
        data["cash_flow"],
    )
    
    stock_data = {
        "Company": info.get("longName", "N/A"),
        "Market Cap ($B)": round(info.get("marketCap", 0) / 1e9, 2),
        "Stock Price ($)": info.get("currentPrice", "N/A"),
        "52-Week High ($)": info.get("fiftyTwoWeekHigh", "N/A"),
        "52-Week Low ($)": info.get("fiftyTwoWeekLow", "N/A"),
        "P/E Ratio": info.get("trailingPE", "N/A"),
        "Revenue ($B)": safe_get(income_stmt, "Total Revenue") / 1e9 if safe_get(income_stmt, "Total Revenue") else "N/A",
        "Net Income ($B)": safe_get(income_stmt, "Net Income") / 1e9 if safe_get(income_stmt, "Net Income") else "N/A",
        "EPS ($)": info.get("trailingEps", "N/A"),
        "Operating Margin (%)": round(info.get("operatingMargins", 0) * 100, 2),
        "Gross Margin (%)": round(info.get("grossMargins", 0) * 100, 2),
        "Return on Equity (ROE) (%)": round(info.get("returnOnEquity", 0) * 100, 2),
        "Return on Assets (ROA) (%)": round(info.get("returnOnAssets", 0) * 100, 2),
        "Debt-to-Equity Ratio": (
            round(safe_get(balance_sheet, "Total Debt") / safe_get(balance_sheet, "Total Stockholder Equity"), 2)
            if safe_get(balance_sheet, "Total Debt") and safe_get(balance_sheet, "Total Stockholder Equity")
            else "N/A"
        ),
        "Free Cash Flow ($B)": safe_get(cash_flow, "Total Cash From Operating Activities") / 1e9
        if safe_get(cash_flow, "Total Cash From Operating Activities")
        else "N/A",
        "Dividend Yield (%)": round(info.get("dividendYield", 0) * 100, 2),  # Fixed percentage format
        "Dividend Rate ($)": info.get("dividendRate", "N/A"),
        "Ex-Dividend Date": info.get("exDividendDate", "N/A"),
        "Payout Ratio (%)": round(info.get("payoutRatio", 0) * 100, 2),
        "5-Year Avg Dividend Yield (%)": round(info.get("fiveYearAvgDividendYield", 0) * 100, 2),
    }
    
    # Return stock data and historical trends
    return stock_data, data.get("history")

def get_stock_overview(ticker):
    """Fetch and return the full stock overview, insights, and historical data."""
    stock_data, history = extract_key_metrics(ticker)
    
    # Convert financial metrics to a DataFrame (transposed for readability)
    financial_df = pd.DataFrame([stock_data]).T
    
    # Prepare data for insights generation
    summary_data = []
    
    # Append key metrics for summarization
    for key, value in stock_data.items():
        summary_data.append(f"{key}: {value}")
    
    # Add historical trends for context
    if history is not None and not history.empty:
        summary_data.append(f"Historical Performance (Last 5 Days): {history.to_dict('records')}")
    
    # Generate financial insights using Gemini
    insights = generate_financial_insights(summary_data)
    
    return financial_df, history, insights

# # Example usage
# ticker = "MSFT"
# financial_summary, historical_data, key_insights = get_stock_overview(ticker)

# # Display results
# print("\n--- Financial Summary ---\n")
# print(financial_summary)

# print("\n--- Historical Data (Last 5 Days) ---\n")
# print(historical_data)

# print("\n--- Key Insights ---\n")
# print(key_insights)
