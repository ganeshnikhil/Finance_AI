import pandas as pd
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from dotenv import load_dotenv
from os import environ
import time 


# Global API key
load_dotenv()
fmp_cloud_key = environ.get("fmp_cloud_key")

def get_press_release(symbol):
    api_link = f"https://fmpcloud.io/api/v3/press-releases/{symbol}?limit=100&apikey={fmp_cloud_key}"
    # Add headers to the request to prevent 403 Forbidden errors
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    req = Request(api_link, headers=headers)
    
    try:
        response = urlopen(req)
        data = response.read()
        return data 
    
    except (HTTPError, URLError) as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None


def get_single_fin_statement(symbol, statement_type):
    """
    Retrieve a specific type of financial statement for a given company.
    
    Args:
        symbol (str): The stock symbol (e.g., 'AAPL').
        statement_type (str): The type of financial statement (e.g., 'income-statement').
        fmp_cloud_key (str): Your FMP Cloud API key.
    
    Returns:
        pd.DataFrame: The financial statement data in a pandas DataFrame.
    """
    # Construct the API link with only annual data and a limit of 120
    api_link = f'https://fmpcloud.io/api/v3/{statement_type}/{symbol}?period=annual&limit=120&apikey={fmp_cloud_key}'
    
    # Add headers to the request to prevent 403 Forbidden errors
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    req = Request(api_link, headers=headers)

    try:
        response = urlopen(req)
        data = response.read()
        df = pd.read_json(data.decode('utf-8'))

        # Drop columns that aren't relevant
        df = df.drop(['link', 'cik'], axis=1, errors='ignore')

        # Add a new column indicating the type of the financial statement
        df['statement_type'] = statement_type
        
        return df

    except (HTTPError, URLError) as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None


def get_period_fin_statements(symbol):
    """
    Retrieve all financial statements (income, balance sheet, cash flow) for a specified company.
    """
    # Fetch each of the three financial statements
    inc_statement = get_single_fin_statement(symbol, 'income-statement')
    bs_statement = get_single_fin_statement(symbol, 'balance-sheet-statement')
    cf_statement = get_single_fin_statement(symbol, 'cash-flow-statement')
    
    # Combine the fetched dataframes horizontally (side by side)
    if inc_statement is None or bs_statement is None or cf_statement is None:
        print("Error: One or more financial statements failed to fetch.")
        return None

    period_fin_statement = pd.concat([inc_statement, bs_statement, cf_statement], axis=1)
    
    # Add a new column indicating the time period of the statements
    period_fin_statement['period_category'] = 'annual'
    
    # Remove any duplicate columns
    period_fin_statement = period_fin_statement.loc[:, ~period_fin_statement.columns.duplicated()]
    
    return period_fin_statement


def single_company_full_financials(symbol):
    """
    Retrieve the complete dataset of historical financial statements for a specified company.
    """
    # Retrieve only annual financial statements
    fin_statement_annual = get_period_fin_statements(symbol)
    
    # If the API request was successful, return the data
    if fin_statement_annual is not None:
        # You could add additional processing or adjustments here
        print("Successfully retrieved the financial statements.")
        return fin_statement_annual
    else:
        print("Failed to retrieve financial statements.")
        return None
