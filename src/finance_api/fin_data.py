import pandas as pd
# from urllib.request import urlopen
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from dotenv import load_dotenv
from os import environ

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
    
    
def get_single_fin_statement(symbol, statement_type, period):
    """
    Retrieve a specific type of financial statement for a given company.
    Args:
        symbol (str): The stock symbol (e.g., 'AAPL').
        statement_type (str): The type of financial statement (e.g., 'income-statement').
        period (str): The period type ('annual' or 'quarter').
        fmp_cloud_key (str): Your FMP Cloud API key.
    Returns:
        pd.DataFrame: The financial statement data in a pandas DataFrame.
    """
    # Define the period type based on user input
    period_type = 'period=annual&' if period.lower() == 'annual' else 'period=quarter&'
    
    # Adjust limit based on the period
    limit = 120 if period.lower() == 'annual' else 400
    
    
    # Construct the API link with given parameters
    #api_link = f'https://fmpcloud.io/api/v3/{statement_type}/{symbol}?{period_type}apikey={fmp_cloud_key}'
    api_link = f'https://fmpcloud.io/api/v3/{statement_type}/{symbol}?limit={limit}&apikey={fmp_cloud_key}'
    # Add headers to the request to prevent 403 Forbidden errors
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Prepare the request with headers
    req = Request(api_link, headers=headers)

    try:
        # Fetch the data from the API
        response = urlopen(req)
        data = response.read()
        
        # Convert the data to JSON and then to a pandas DataFrame
        df = pd.read_json(data.decode('utf-8'))

        # Drop columns that aren't relevant, if they exist
        try:
            df = df.drop(['link', 'cik'], axis=1)
        except KeyError:
            pass

        # Append a new column indicating the type of the financial statement
        df['statement_type'] = statement_type
        
        return df

    except HTTPError as e:
        print(f"HTTP error occurred: {e.code} - {e.reason}")
        return None
    except URLError as e:
        print(f"URL error occurred: {e.reason}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def get_period_fin_statements(symbol, period):
    """
    Retrieve all financial statements (income, balance sheet, cash flow) for a specified company.
    """
    # Fetch each of the three financial statements
    inc_statement = get_single_fin_statement(symbol, 'income-statement', period)
    bs_statement = get_single_fin_statement(symbol, 'balance-sheet-statement', period)
    cf_statement = get_single_fin_statement(symbol, 'cash-flow-statement', period)
    
    # Combine the fetched dataframes horizontally (side by side)
    period_fin_statement = pd.concat([inc_statement, bs_statement, cf_statement], axis=1)
    
    # Add a new column indicating the time period of the statements
    period_fin_statement['period_category'] = period
    
    # Remove any duplicate columns
    period_fin_statement = period_fin_statement.loc[:, ~period_fin_statement.columns.duplicated()]
    
    return period_fin_statement

def trailingTwelveFins(df, inc_statement=True):
    """
    Compute the trailing twelve months (TTM) financial data from quarterly financial statements.
    """
    print(df)
    # Columns that do not change in the TTM calculation
    columns_unchanged = [
        'symbol', 'reportedCurrency', 'period', 'date', 'fillingDate', 
        'acceptedDate', 'calendarYear', 'period_category', 'statement_type'
    ]
    data_unchanged = df[columns_unchanged]
    df = df.drop(columns=columns_unchanged, errors='ignore')
    
    if inc_statement:
        # Columns in the income statement that will be averaged
        columns_averaged = ['weightedAverageShsOut', 'weightedAverageShsOutDil']
        data_averaged = df[columns_averaged].mean(axis=0)
    else:
        data_averaged = None

    # Sum other columns for TTM
    data_summed = df.sum(axis=0)
    
    # Combine unchanged, summed, and averaged data
    result_df = pd.concat([data_unchanged, data_summed, data_averaged], axis=1)
    return result_df

def financial_adjustments(df):
    """
    Adjust financial data to provide more derived metrics.
    """
    # Compute adjusted operating income
    df['adjusted_operatingIncome'] = df['revenue'] - df['costOfRevenue'] - df['operatingExpenses']
    
    # Compute adjusted EBITDA
    df['adjusted_ebitda'] = df['adjusted_operatingIncome'] + df['depreciationAndAmortization']
    
    # Compute adjusted earnings
    df['adjusted_earnings'] = df['netIncome'] - (df['totalOtherIncomeExpensesNet'] + df['interestExpense'])
    
    # Compute adjusted EPS
    df['adjusted_eps'] = df['adjusted_earnings'] / df['weightedAverageShsOutDil']
    
    # Compute FFO (Funds from Operations)
    df['funds_from_operations_FFO'] = df['operatingCashFlow'] - df['changeInWorkingCapital']
    
    # Compute FFO per share
    df['funds_from_operations_FFO_per_share'] = df['funds_from_operations_FFO'] / df['weightedAverageShsOutDil']
    
    # Compute free cash flow per share
    df['freeCashFlow_per_share'] = df['freeCashFlow'] / df['weightedAverageShsOutDil']
    
    # Compute operating cash flow per share
    df['operatingCashFlow_per_share'] = df['operatingCashFlow'] / df['weightedAverageShsOutDil']
    
    # Compute adjusted EBITDA Margin
    df['adjusted_ebitda_margin'] = df['adjusted_ebitda'] / df['revenue']
    
    # Compute adjusted earnings margin
    df['adjusted_earnings_margin'] = df['adjusted_earnings'] / df['revenue']
    
    return df

def single_company_full_financials(symbol):
    """
    Retrieve the complete dataset of historical financial statements for a specified company.
    """
    # Retrieve annual financial statements
    fin_statement_annual = get_period_fin_statements(symbol, 'Annual')
    
    # Retrieve quarterly financial statements
    fin_statement_quarterly = get_period_fin_statements(symbol, 'Quarter')
    
    # Calculate the trailing twelve months (TTM) financials
    inc_ttm = trailingTwelveFins(fin_statement_quarterly[fin_statement_quarterly['statement_type'] == 'income-statement'], inc_statement=True)
    cf_ttm = trailingTwelveFins(fin_statement_quarterly[fin_statement_quarterly['statement_type'] == 'cash-flow-statement'], inc_statement=False)
    
    # Consolidate TTM financial statements
    fin_statement_ttm = pd.concat([inc_ttm, cf_ttm], ignore_index=True)
    
    # Merge annual, quarterly, and TTM financial statements
    full_fin_statement = pd.concat([fin_statement_annual, fin_statement_quarterly, fin_statement_ttm])
    
    # Reset index for the consolidated dataframe
    full_fin_statement.reset_index(drop=True, inplace=True)
    
    # Compute and add derived financial metrics
    full_fin_statement = financial_adjustments(full_fin_statement)
    
    return full_fin_statement




