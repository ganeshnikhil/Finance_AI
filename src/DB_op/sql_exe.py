import sqlite3
import logging
from src.DB_op.sql_filter import is_read_only_sql



def execute_sql_query(db_path, query, params=None):
    """
    Executes a read-only SQL query on the given SQLite database and includes fields in the result.

    Args:
        db_path (str): Path to the SQLite database.
        query (str): The SQL query to execute.
        params (tuple): Optional parameters for parameterized queries.

    Returns:
        dict: A dictionary containing the success status, results, fields, and any error messages.
    """
    if not is_read_only_sql(query):
        logging.warning("Query validation failed. Potential risk detected.")
        return {
            "success": False,
            "fields": [],
            "results": [],
            "error": "Bad Query. Potential risk detected."
        }
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        logging.info(f"Connected to database: {db_path}")

        # Execute the query with parameters (if provided)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # Fetch results
        results = cursor.fetchall()
        
        # Fetch column names
        fields = [description[0] for description in cursor.description]
        logging.info("Query executed successfully. Results and fields fetched.")

        return {
            "success": True,
            "fields": fields,
            "results": results,
            "error": None
        }

    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return {
            "success": False,
            "fields": [],
            "results": [],
            "error": str(e)
        }

    finally:
        # Close the database connection
        if conn:
            conn.close()
            logging.info("Database connection closed.")


