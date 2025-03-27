from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
#from langchain_ollama import ChatOllama
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.Brain.ask_gemini import get_ticker_symbol
from src.DB_op.sql_filter import get_missing_tables 
from src.DB_op.load_db import load_finance_to_db
import getpass
import os
from dotenv import load_dotenv
from os import environ
import logging 


DB_PATH = "./Data/financial_Db.db"


def load_database():
    """Loads the SQLite database using LangChain."""
    return SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

def load_environment():
    """Loads environment variables for API keys."""
    load_dotenv()
    genai_key = environ.get("genai_key")
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = genai_key

def initialize_llm():
    """Initializes the Gemini LLM with Flash-Lite model."""
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

def create_embedding_model():
    """Creates an embedding model for semantic similarity."""
    #EMBEDDING_MODEL = "nomic-embed-text"
    EMBEDDING_MODEL = "models/embedding-001"
    return GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    #return OllamaEmbeddings(model=EMBEDDING_MODEL)


def get_examples():
    """Returns a list of example queries and SQL responses for few-shot prompting."""
    return [
        {"input": "What was Apple's total revenue in 2023?", "query": "SELECT `Total Revenue` FROM AAPL WHERE year = '2023';"},
        {"input": "Find Google's net income for the most recent year.", "query": "SELECT `Net Income` FROM GOOGL ORDER BY year DESC LIMIT 1;"},
        {"input": "What was Reliance's operating income in 2022?", "query": "SELECT `Operating Income` FROM `RELIANCE.NS` WHERE year = '2022';"},
        {"input": "List Apple's research and development expenses for the last 3 years.", "query": "SELECT year, `Research And Development` FROM AAPL ORDER BY year DESC LIMIT 3;"},
        {"input": "Show Google's total assets for each year.", "query": "SELECT year, `Total Assets` FROM GOOGL;"},
        {"input": "What was Reliance's diluted EPS in the latest year?", "query": "SELECT `Diluted EPS` FROM `RELIANCE.NS` ORDER BY year DESC LIMIT 1;"},
        {"input": "Find Apple's gross profit in 2021.", "query": "SELECT `Gross Profit` FROM AAPL WHERE year = '2021';"},
        {"input": "What was Google's free cash flow in the year 2020?", "query": "SELECT `Free Cash Flow` FROM GOOGL WHERE year = '2020';"},
        {"input": "List Reliance's capital expenditure for all years.", "query": "SELECT year, `Capital Expenditure` FROM `RELIANCE.NS`;"},
        {"input": "What were Apple's total liabilities in 2022?", "query": "SELECT `Total Liabilities Net Minority Interest` FROM AAPL WHERE year = '2022';"},
        {"input": "Show Google's depreciation and amortization in the most recent year.", "query": "SELECT `Depreciation And Amortization` FROM GOOGL ORDER BY year DESC LIMIT 1;"},
        {"input": "What was Reliance's cost of revenue in the year 2023?", "query": "SELECT `Cost Of Revenue` FROM `RELIANCE.NS` WHERE year = '2023';"},
        {"input": "Get Apple's net income from continuing operations for all years.", "query": "SELECT year, `Net Income From Continuing Operations` FROM AAPL;"},
        {"input": "Find Google's selling general and administrative expenses in 2021.", "query": "SELECT `Selling General And Administration` FROM GOOGL WHERE year = '2021';"},
        {"input": "What was Reliance's cash and cash equivalents in 2020?", "query": "SELECT `Cash And Cash Equivalents` FROM `RELIANCE.NS` WHERE year = '2020';"},
        {"input": "Show Apple's total debt for the year 2024.", "query": "SELECT `Total Debt` FROM AAPL WHERE year = '2024';"},
        {"input": "What was Google's tax provision in the latest year?", "query": "SELECT `Tax Provision` FROM GOOGL ORDER BY year DESC LIMIT 1;"},
        {"input": "List Reliance's operating expense for each year.", "query": "SELECT year, `Operating Expense` FROM `RELIANCE.NS`;"},
        {
            "input": "Which company had the highest cash dividend return in 2023?",
            "query": """
            SELECT company, "Cash Dividends Paid"
            FROM (
                SELECT 'AAPL' as company, "Cash Dividends Paid" FROM AAPL WHERE year = '2023'
                UNION ALL
                SELECT 'GOOGL' as company, NULL as "Cash Dividends Paid" FROM GOOGL WHERE year = '2023'
                UNION ALL
                SELECT 'RELIANCE.NS' as company, "Cash Dividends Paid" FROM `RELIANCE.NS` WHERE year = '2023'
            ) AS combined_dividends
            ORDER BY "Cash Dividends Paid" DESC
            LIMIT 1;
            """
        },
        {
            "input": "Compare the revenue and net income of Apple and Google for the year 2023.",
            "query": """
            SELECT
                'AAPL' AS company,
                "Total Revenue" AS revenue,
                "Net Income" AS net_income
            FROM AAPL
            WHERE year = '2023'

            UNION ALL

            SELECT
                'GOOGL' AS company,
                "Total Revenue" AS revenue,
                "Net Income" AS net_income
            FROM GOOGL
            WHERE year = '2023';
            """
        }
    ]


def get_examples():
    """Returns a list of example queries and SQL responses for few-shot prompting."""
    return [
        {"input": "List all years in the dataset.", "query": "SELECT DISTINCT year FROM 'company1';"},
        {"input": "Find the maximum revenue.", "query": "SELECT MAX(`Total Revenue`) FROM 'company1';"},
        {"input": "Find the average net income.", "query": "SELECT AVG(`Net Income`) FROM 'company1';"},
        {"input": "Show the total assets for a specific year.", "query": "SELECT `Total Assets` FROM 'company1' WHERE year = '2023';"},
        {"input": "List the research and development expenses for the last 3 years.", "query": "SELECT year, `Research And Development` FROM company1 ORDER BY year DESC LIMIT 3;"},
        {"input": "Show the total assets for each year.", "query": "SELECT year, `Total Assets` FROM 'company1';"},
        {"input": "What was the diluted EPS in the latest year?", "query": "SELECT `Diluted EPS` FROM 'company1' ORDER BY year DESC LIMIT 1;"},
        {"input": "Find the gross profit in a specific year.", "query": "SELECT `Gross Profit` FROM 'company1' WHERE year = '2021';"},
        {"input": "What was the free cash flow in a specific year?", "query": "SELECT `Free Cash Flow` FROM 'company1' WHERE year = '2020';"},
        {"input": "List the capital expenditure for all years.", "query": "SELECT year, `Capital Expenditure` FROM 'company1';"},
        {"input": "What were the total liabilities in a specific year?", "query": "SELECT `Total Liabilities Net Minority Interest` FROM 'company1' WHERE year = '2022';"},
        {"input": "Show the depreciation and amortization in the most recent year.", "query": "SELECT `Depreciation And Amortization` FROM 'company1' ORDER BY year DESC LIMIT 1;"},
        {"input": "What was the cost of revenue in a specific year?", "query": "SELECT `Cost Of Revenue` FROM 'company1' WHERE year = '2023';"},
        {"input": "Get the net income from continuing operations for all years.", "query": "SELECT year, `Net Income From Continuing Operations` FROM 'company1';"},
        {"input": "Find the selling general and administrative expenses in a specific year.", "query": "SELECT `Selling General And Administration` FROM 'company1' WHERE year = '2021';"},
        {"input": "What was the cash and cash equivalents in a specific year?", "query": "SELECT `Cash And Cash Equivalents` FROM 'company1' WHERE year = '2020';"},
        {"input": "Show the total debt for a specific year.", "query": "SELECT `Total Debt` FROM 'company1' WHERE year = '2024';"},
        {"input": "What was the tax provision in the latest year?", "query": "SELECT `Tax Provision` FROM 'company1' ORDER BY year DESC LIMIT 1;"},
        {"input": "List the operating expense for each year.", "query": "SELECT year, `Operating Expense` FROM 'company1';"},
        {
            "input": "Which company had the highest cash dividend return in 2023?",
            "query": """
            SELECT company, "Cash Dividends Paid"
            FROM (
                SELECT 'company1' as company, "Cash Dividends Paid" FROM company1 WHERE year = '2023'
                UNION ALL
                SELECT 'company2' as company, NULL as "Cash Dividends Paid" FROM company2 WHERE year = '2023'
                UNION ALL
                SELECT 'company3' as company, "Cash Dividends Paid" FROM company3 WHERE year = '2023'
            ) AS combined_dividends
            ORDER BY "Cash Dividends Paid" DESC
            LIMIT 1;
            """
        },
        {
            "input": "Compare the revenue and net income of two companies for a specific year.",
            "query": """
            SELECT
                'company1' AS company,
                "Total Revenue" AS revenue,
                "Net Income" AS net_income
            FROM company1
            WHERE year = '2023'

            UNION ALL

            SELECT
                'company2' AS company,
                "Total Revenue" AS revenue,
                "Net Income" AS net_income
            FROM company2
            WHERE year = '2023';
            """
        },
        {
            "input": "Find the average of a specific metric.",
            "query": "SELECT AVG(`Metric1`) FROM 'company1';"
        },
        {
            "input": "Find the sum of a specific metric.",
            "query": "SELECT SUM(`Metric1`) FROM 'company1';"
        },
        {
            "input": "Find the count of rows.",
            "query": "SELECT COUNT(*) FROM 'company1';"
        },
        {
            "input": "find the min of a specific metric",
            "query": "SELECT MIN(`Metric1`) FROM 'company1';"
        },
        {
            "input": "find the max of a specific metric",
            "query": "SELECT MAX(`Metric1`) FROM 'company1';"
        },
        {
            "input": "find the average of a specific metric for each year",
            "query": "SELECT year, AVG(`Metric1`) FROM 'company1' GROUP BY year;"
        },
        {
            "input": "find the sum of a specific metric for each year",
            "query": "SELECT year, SUM(`Metric1`) FROM 'company1' GROUP BY year;"
        },
        {
            "input": "find the count of rows for each year",
            "query": "SELECT year, COUNT(*) FROM 'company1' GROUP BY year;"
        },
        {
            "input": "find the min of a specific metric for each year",
            "query": "SELECT year, MIN(`Metric1`) FROM 'company1' GROUP BY year;"
        },
        {
            "input": "find the max of a specific metric for each year",
            "query": "SELECT year, MAX(`Metric1`) FROM 'company1' GROUP BY year;"
        },
        {
            "input": "Compare two metrics for a specific company",
            "query": "SELECT `Metric1`,`Metric2` FROM 'company1' WHERE year = '2023';"
        }
    ]
def create_example_selector(examples, embedding):
    """Creates a few-shot example selector using semantic similarity."""
    return SemanticSimilarityExampleSelector.from_examples(
        examples,
        embedding,
        FAISS,
        k=5,
        input_keys=["input"],
    )

system_prefix = """You are a financial SQL query agent interacting with a corporate database.
Given an input question, create an optimized SQL query that retrieves relevant financial data.
Ensure that the query aligns with best practices for performance and correctness.

⚠️ IMPORTANT:
- The table name is always the same as the company's ticker symbol.
- DO NOT use the company name directly in the query. 
- ALWAYS map the company name to its ticker symbol before constructing the query.
- Indian companies listed on NSE should have '.NS' appended to the ticker symbol (e.g., RELIANCE → RELIANCE.NS).

✅ Your task involves:
1. Understanding the user's financial query.
2. Identifying the correct ticker symbol from the provided company name.
3. Generating a valid SQL query using the ticker symbol as the table name.
4. Ensuring that the SQL query is syntactically correct and optimized for performance.

🔍 Examples of User Inputs and Corresponding SQL Queries:

1. **User Input:**  
   "What was the revenue of Google last year?"  
   **SQL Query:**  
   ```sql
   SELECT revenue
   FROM GOOGL
   WHERE year = YEAR(CURRENT_DATE) - 1;
"""
def create_few_shot_prompt(example_selector):
    """Creates a few-shot prompt template using examples."""
    # system_prefix = """You are a financial SQL query agent interacting with a corporate database.
    # Given an input question, create an optimized SQL query that retrieves relevant financial data.
    # Ensure that the query aligns with best practices for performance and correctness.
    # IMPORTANT: table name is same as company's ticker symbol.(dont use direct compnay name provided in query instead use ticker symbol.)
    # Here are some examples of user inputs and their corresponding SQL queries:"""

    return FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=PromptTemplate.from_template(
            "User input: {input}\nSQL query: {query}"
        ),
        input_variables=["input", "dialect", "top_k"],
        prefix=system_prefix,
        suffix="",
    )

def create_full_prompt(few_shot_prompt):
    """Generates a full prompt template for the agent."""
    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=few_shot_prompt),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

def create_agent(llm, db, full_prompt):
    """Creates a LangChain SQL agent with the given model and database."""
    return create_sql_agent(
        llm=llm,
        db=db,
        prompt=full_prompt,
        verbose=True,
        agent_type="openai-tools",
    )

def data_analysis(query: str) -> str:
    """Main function to perform financial data analysis."""
    ticker_symbols = get_ticker_symbol(query)
    
    # Check for missing tables and load missing data
    database_response = get_missing_tables(DB_PATH, ticker_symbols)

    if database_response.get("success"):
        missing_tables = database_response.get("missing_tables", [])
        if missing_tables:
            load_finance_to_db(missing_tables)
            logging.info(f"Loaded missing tables: {missing_tables}")
        else:
            logging.info("No missing tables found.")
    else:
        logging.error(f"Error checking tables: {database_response.get('error')}")
        return "Error in database operations."

    # Load environment variables and setup
    load_environment()
    db = load_database()
    llm = initialize_llm()
    embedding = create_embedding_model()
    examples = get_examples()
    example_selector = create_example_selector(examples, embedding)
    few_shot_prompt = create_few_shot_prompt(example_selector)
    full_prompt = create_full_prompt(few_shot_prompt)
    agent = create_agent(llm, db, full_prompt)

    # Get SQL response from agent
    response = agent.invoke({"input": query})
    print(response)
    return response.get("output")

if __name__ == "__main__":
    query = ""
    data_analysis(query)

# def data_analysis(query:str) -> str :
#     ticker_symbols = get_ticker_symbol(query)
#     databse_response = get_missing_tables(ticker_symbols)
    
#     if databse_response.get("success"):
#         missing_tables = databse_response.get("missing_table")
#         load_finance_to_db(missing_tables)
        
#     load_environment()
#     db = load_database()
#     llm = initialize_llm()
#     embedding = create_embedding_model()
#     examples = get_examples()
#     example_selector = create_example_selector(examples, embedding)
#     few_shot_prompt = create_few_shot_prompt(example_selector)
#     full_prompt = create_full_prompt(few_shot_prompt)
#     agent = create_agent(llm, db, full_prompt)
#     response = agent.invoke({"input":query})
#     return response 

# if __name__ == "__main__":
#     query = ""
#     data_analysis(query)
