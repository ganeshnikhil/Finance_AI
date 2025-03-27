import sqlite3
import pandas as pd
from src.finance_api.yh_fn import single_company_full_financials


def create_database(db_name="financal_DB.db"):
    """
    Create or connect to a SQLite database.
    
    Parameters:
    - db_name (str): Name of the SQLite database file.
    
    Returns:
    - conn (sqlite3.Connection): Connection object to the SQLite database.
    """
    conn = sqlite3.connect(db_name)
    return conn


def create_table_from_df(conn, df, table_name):
    """
    Create a SQLite table based on the structure of a pandas DataFrame.
    
    Parameters:
    - conn (sqlite3.Connection): Connection object to the SQLite database.
    - df (pd.DataFrame): DataFrame containing the data to load.
    - table_name (str): Name of the table to create.
    """
    # Create a table if it doesn't already exist
    df.to_sql(table_name, conn, if_exists="fail", index=False)
    print(f"Table '{table_name}' created successfully in the database.")


def insert_data_to_table(conn, df, table_name):
    """
    Insert data from a pandas DataFrame into an existing SQLite table.
    
    Parameters:
    - conn (sqlite3.Connection): Connection object to the SQLite database.
    - df (pd.DataFrame): DataFrame containing the data to insert.
    - table_name (str): Name of the table where data will be inserted.
    """
    try:
        df.to_sql(table_name, conn, if_exists="append", index=False)
        print(f"Data inserted successfully into table '{table_name}'.")
    except Exception as e:
        print(f"Error inserting data into table '{table_name}': {e}")


def load_financials_to_db(df, company_symbol, db_name="financial_DB.db"):
    """
    Load a pandas DataFrame into a SQLite database table named after the company symbol.
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing the financial data.
    - company_symbol (str): Ticker symbol of the company (used as table name).
    - db_name (str): Name of the SQLite database file.
    """
    # Step 1: Create or connect to the database
    conn = create_database(db_name)
    
    try:
        # Step 2: Check if the table already exists
        table_exists_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{company_symbol}';"
        cursor = conn.cursor()
        cursor.execute(table_exists_query)
        table_exists = cursor.fetchone() is not None
        
        if table_exists:
            # If the table exists, insert the data into the existing table
            insert_data_to_table(conn, df, company_symbol)
        else:
            # If the table doesn't exist, create it and insert data
            create_table_from_df(conn, df, company_symbol)
    
    except Exception as e:
        print(f"Error handling table for '{company_symbol}': {e}")
    finally:
        # Step 3: Close the connection
        conn.close()
        print(f"Connection to database '{db_name}' closed.")

def load_finance_to_db(ticker_list:list) -> None:
    for symbol in ticker_list:
        data = single_company_full_financials(symbol)  # Get financial data
        if data is not None and not data.empty:
            # Insert or create table based on whether it already exists in the database
            load_financials_to_db(data, symbol)
            print(f"{symbol} Done...")
    return None 


# Example Usage
if __name__ == "__main__":
    
    # Load the data into the SQLite database
    cmp_list = ["AAPL","GOOGL","RELIANCE.NS"]
    for symbol in cmp_list:
        data = single_company_full_financials(symbol)  # Get financial data
        if data is not None and not data.empty:
            # Insert or create table based on whether it already exists in the database
            load_financials_to_db(data, symbol)
            print(f"{symbol} Done...")
        else:
            print("No data found...")
