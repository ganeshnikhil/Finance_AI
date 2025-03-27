import re
import sqlite3
import logging 


def is_read_only_sql(query):
    """
    Check if the SQL query is a read-only operation (i.e., only SELECT).
    
    Parameters:
    - query (str): The SQL query to validate.
    
    Returns:
    - bool: True if the query is read-only, False if it's not.
    """
    # Convert the query to lowercase to make it case-insensitive
    query = query.strip().lower()
    
    # Check if query starts with SELECT and contains only SELECT-related operations
    if query.startswith("select"):
        # List of forbidden SQL operations (modifying queries)
        forbidden_keywords = ["insert", "update", "delete", "drop", "alter", "truncate", "replace", "merge"]
        
        # Search for forbidden keywords anywhere in the query (case-insensitive)
        for keyword in forbidden_keywords:
            if keyword in query:
                return False
        
        # Optionally check if there's a suspicious use of "into" (as used in SELECT INTO or INSERT)
        if "into" in query and not query.startswith("select into"):
            return False
        
        # Optionally check for a WHERE clause with potential write operations (not necessary for all cases)
        if re.search(r"\bset\b", query):  # "SET" is typical for UPDATE queries
            return False
        
        return True
    else:
        return False



def get_missing_tables(db_path, table_names):
    """
    Checks if the specified tables exist in the given SQLite database and returns the missing tables.

    Args:
        db_path (str): Path to the SQLite database.
        table_names (list): List of table names to check.

    Returns:
        dict: A dictionary containing the success status, missing tables, and any error messages.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        logging.info(f"Connected to database: {db_path}")
        
        missing_tables = []
        
        # Check if each table exists
        for table in table_names:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            result = cursor.fetchone()
            
            if not result:
                missing_tables.append(table)
        
        logging.info("Table existence check completed.")
        
        return {
            "success": True,
            "missing_tables": missing_tables,
            "error": None
        }

    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return {
            "success": False,
            "missing_tables": [],
            "error": str(e)
        }

    finally:
        # Close the database connection
        if conn:
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    # Example Usage:
    query = "SELECT * FROM employees WHERE employee_id = 101"
    print(is_read_only_sql(query))  # Should return True (it's a read-only query)

    query = "INSERT INTO employees (name, position) VALUES ('John', 'Manager')"
    print(is_read_only_sql(query))  # Should return False (it's a write query)

    query = "UPDATE employees SET position = 'Senior Manager' WHERE employee_id = 101"
    print(is_read_only_sql(query))  # Should return False (it's a write query)
