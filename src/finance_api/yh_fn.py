import yfinance as yf
import pandas as pd
from datetime import datetime


def get_single_fin_statement(symbol, statement_type, period='annual'):
    """
    Retrieve a specific type of financial statement for a given company using Yahoo Finance.
    
    Args:
        symbol (str): The stock symbol (e.g., 'AAPL').
        statement_type (str): The type of financial statement (e.g., 'income-statement').
        period (str): The period for the financial data ('annual' or 'quarterly').
    
    Returns:
        pd.DataFrame: The financial statement data in a pandas DataFrame.
    """
    # Fetch data from Yahoo Finance
    stock = yf.Ticker(symbol)

    if statement_type == 'income-statement':
        df = stock.financials.transpose()  # Yahoo Finance income statement data
    elif statement_type == 'balance-sheet-statement':
        df = stock.balance_sheet.transpose()  # Yahoo Finance balance sheet data
    elif statement_type == 'cash-flow-statement':
        df = stock.cashflow.transpose()  # Yahoo Finance cash flow data
    else:
        print(f"Invalid statement type: {statement_type}")
        return None
    return df

def get_period_fin_statements(symbol, period='annual'):
    """
    Retrieve all financial statements (income, balance sheet, cash flow) for a specified company.
    """
    # Fetch each of the three financial statements
    inc_statement = get_single_fin_statement(symbol, 'income-statement', period)
    bs_statement = get_single_fin_statement(symbol, 'balance-sheet-statement', period)
    cf_statement = get_single_fin_statement(symbol, 'cash-flow-statement', period)

    # Check if any statement failed to fetch
    if inc_statement is None or bs_statement is None or cf_statement is None:
        print("Error: One or more financial statements failed to fetch.")
        return None

    # Combine the fetched dataframes horizontally (side by side) while preserving the index
    period_fin_statement = pd.concat([inc_statement, bs_statement, cf_statement], axis=1, ignore_index=False)
    
    # Add a new column indicating the time period of the statements
    period_fin_statement['period_category'] = period  # Add period category column
    
    # Convert the index to string to use the .str accessor
    period_fin_statement.index = period_fin_statement.index.astype(str)
    
    
    # Convert the index to string to use the .str accessor
    period_fin_statement.index = period_fin_statement.index.astype(str)

    # Extract the year from the index and create a new column
    period_fin_statement['year'] = period_fin_statement.index.str.split('-').str[0]

    # Reset the index to make it a default integer index
    period_fin_statement = period_fin_statement.reset_index(drop=True)

    # Return the modified DataFrame
    return period_fin_statement


    # # Extract the year from the index and create a new column
    # period_fin_statement['index'] = period_fin_statement.index.str.split('-').str[0]

    # # # Print out the raw index to debug the filtering issue
    # # print(f"Index for {statement_type}: {df.index}")
    # # # Reset the index to make the date a column
    # period_fin_statement = period_fin_statement.reset_index()
    # period_fin_statement.rename(columns={"index": "year"}, inplace=True)  # Ren
    # return period_fin_statement

def single_company_full_financials(symbol, period='annual'):
    """
    Retrieve the complete dataset of financial statements for a specified company.
    """
    fin_statement = get_period_fin_statements(symbol, period)

    if fin_statement is not None:
        print("Successfully retrieved the financial statements.")
        return fin_statement
    else:
        print("Failed to retrieve financial statements.")
        return None

def format_yfinance_news(raw_news_data):
    """
    Format the raw news data retrieved from Yahoo Finance into a structured format.
    
    Args:
        raw_news_data (list): List of raw news articles from Yahoo Finance API.
        
    Returns:
        list: A list of formatted dictionaries containing news article details.
    """
    formatted_news = []
    
    for article in raw_news_data:
        content = article.get('content', {})
        formatted_article = {
            "title": content.get('title', "No Title"),
            "summary": content.get('summary', "No Summary"),
            "published": content.get('pubDate', "Unknown Date"),
            # "url": content.get('canonicalUrl', {}).get('url', "No URL"),
            #"provider": content.get('provider', {}).get('displayName', "Unknown Publisher"),
            #"thumbnail_url": content.get('thumbnail', {}).get('originalUrl', "No Thumbnail"),
        }
        
        formatted_news.append(formatted_article)
    
    return formatted_news


def get_company_news(ticker_symbol):
    """
    Fetches recent news articles related to a company using yfinance.

    Args:
        ticker_symbol (str): The stock ticker symbol of the company (e.g., 'AAPL' for Apple Inc.).

    Returns:
        list: A list of dictionaries containing news articles with title, publisher, publish time, and link.
    """
    try:
        # Get the Ticker object
        ticker = yf.Ticker(ticker_symbol)
        
        # Fetch news articles
        news = ticker.news
        return news 
    
    except Exception as e:
        print(f"Error fetching news for {ticker_symbol}: {e}")
        return []


# Example Usage
if __name__ == "__main__":
    company_symbol = "AAPL"  # Example stock symbol (Apple)
    article = get_company_news(company_symbol)
    for news in format_yfinance_news(article):
        print(news)
        print("\n")
    #print(article)
    # data = single_company_full_financials(company_symbol, period='annual')  # 'quarterly' for quarterly data
    # fields = list(data.columns)
    # print(fields)
    # if data is not None and not data.empty:
    #     ...
    # else:
    #     print("Failed to retrieve financial data.")
