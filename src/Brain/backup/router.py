# from google import genai
# from google.genai import types
# from dotenv import load_dotenv
# from os import environ

# # Load environment variables
# load_dotenv()
# genai_key = environ.get("genai_key")

# ALL_FUNCTIONS = {
#     "tools": [
#         {
#             "name": "rag_query_resolver",
#             "description": "Retrieve precise and contextually relevant financial information from a curated knowledge base. This tool excels at providing accurate answers to specific financial questions about markets, companies, and economic indicators, using structured and validated data.",
#             "parameters": {
#                 "type": "OBJECT",
#                 "properties": {
#                     "query": {"type": "STRING"}
#                 },
#                 "required": ["query"]
#             }
#         },
#         {
#             "name": "data_analysis",
#             "description": "Perform advanced data analysis and provide insights using stored numerical financial datasets. This includes statistical analysis, pattern recognition, comparison, financial data and financial modeling.",
#             "parameters": {
#                 "type": "OBJECT",
#                 "properties": {
#                     "query": {"type": "STRING"}
#                 },
#                 "required": ["query"]
#             }
#         },
#         {
#             "name": "function_calling",
#             "description": "Execute specific functions to retrieve Live market data, News, financial calculations etc. Automate workflows and integrate with external systems.",
#             "parameters": {
#                 "type": "OBJECT",
#                 "properties": {
#                     "query": {"type": "STRING"}
#                 },
#                 "required": ["query"]
#             }
#         },
#         {
#             "name": "direct_gemini_interaction",
#             "description": "Engage in general conversations and access a broad spectrum of internet-accessible information, including general internet-based information.",
#             "parameters": {
#                 "type": "OBJECT",
#                 "properties": {
#                     "query": {"type": "STRING"}
#                 },
#                 "required": ["query"]
#             }
#         },
#     ]
# }

# {
# "examples": [
#     {
#         "query": "What is the current price of Apple stock (AAPL)?",
#         "function_call": "function_calling",
#         "args": { "query": "AAPL" }
#     },
#     {
#         "query": "Who is the CEO of JPMorgan Chase?",
#         "function_call": "rag_query_resolver",
#         "args": { "query": "JPMorgan Chase CEO" }
#     },
#     {
#         "query": "Analyze the revenue growth of Microsoft (MSFT) over the past 5 years.",
#         "function_call": "data_analysis",
#         "args": { "query": "Microsoft revenue growth last 5 years" }
#     },
#     {
#         "query": "Get the real-time stock quote for Google (GOOG).",
#         "function_call": "function_calling",
#         "args": { "query": "GOOG" }
#     },
#     {
#         "query": "What are some interesting facts about the history of finance?",
#         "function_call": "direct_gemini_interaction",
#         "args": { "query": "history of finance facts" }
#     },
#     {
#         "query": "Compare the profitability of Amazon (AMZN) and Walmart (WMT) based on their operating margins.",
#         "function_call": "data_analysis",
#         "args": { "query": "Amazon vs Walmart operating margins" }
#     },
#     {
#         "query": "Fetch the latest news headlines related to the Federal Reserve.",
#         "function_call": "function_calling",
#         "args": { "query": "Federal Reserve latest news" }
#     },
#     {
#         "query": "Summarize the main points of the latest scientific breakthrough.",
#         "function_call": "direct_gemini_interaction",
#         "args": { "query": "latest scientific breakthrough summary" }
#     },
#     {
#         "query": "Retrieve the historical stock data for Bitcoin (BTC) for the last month.",
#         "function_call": "function_calling",
#         "args": { "query": "BTC historical data last month" }
#     },
#     {
#         "query": "Explain the key factors influencing the recent inflation rate.",
#         "function_call": "rag_query_resolver",
#         "args": { "query": "recent inflation rate key factors" }
#     },
#     {
#         "query": "What are the best investment strategies for a volatile market?",
#         "function_call": "rag_query_resolver",
#         "args": { "query": "best investment strategies for volatility" }
#     }
#   ]
# }

# # Configure Gemini client
# client = genai.Client(api_key=genai_key)

# def function_call_gem(query: str) -> list:
#     """
#     Calls Gemini AI with the provided query and retrieves function calls.
#     """
#     client = genai.Client(api_key=genai_key)
    
#     # Convert tools into a format Gemini can understand
#     config = types.GenerateContentConfig(
#         tools=[types.Tool(function_declarations=ALL_FUNCTIONS["tools"])]
#     )
    
#     try:
#         response = client.models.generate_content(
#             model='gemini-2.0-flash',
#             contents=[{"role":"system" , "parts": [{"text": str(examples)}]}] , {"role": "user", "parts": [{"text": query}]}],
#             config=config
#         )
#         return response.function_calls  # Returns the list of function calls
#     except Exception as e:
#         print(f"Error: {e}")
#         return []



# query_examples = [
#     # rag_query_resolver
#     "What is the current price of Apple stock (AAPL)?",
#     "Explain the key factors influencing the recent inflation rate.",
#     "What are the major differences between a bond and a stock?",
#     "Provide a summary of the latest earnings report for Tesla (TSLA).",
#     "Who is the CEO of JPMorgan Chase?",
#     "What is the GDP of the United States?",

#     # data_analysis
#     "Analyze the revenue growth of Microsoft (MSFT) over the past 5 years.",
#     "Compare the profitability of Amazon (AMZN) and Walmart (WMT) based on their operating margins.",
#     "Show me the debt-to-equity ratio for all companies in the technology sector.",
#     "What are the top 10 companies by market capitalization in the healthcare sector?",
#     "Calculate the average return on equity for companies within the S&P 500 financial sector during the last quarter.",
#     "Give me a trend analysis of the cash flow of Alphabet (GOOGL) over the last 3 years.",

#     # function_calling
#     "Get the real-time stock quote for Google (GOOG).",
#     "Retrieve the historical stock data for Bitcoin (BTC) for the last month.",
#     "Calculate the present value of $10,000 in 5 years at an interest rate of 6%.",
#     "Generate a financial report summarizing the current market trends.",
#     "Fetch the latest news headlines related to the Federal Reserve.",
#     "Convert 100 Euros to US Dollars.",

#     # direct_gemini_interaction
#     "What are some interesting facts about the history of finance?",
#     "Explain the concept of artificial intelligence in simple terms.",
#     "Write a short poem about the stock market.",
#     "What are the best places to travel in Europe?",
#     "Summarize the main points of the latest scientific breakthrough.",
#     "What are the ethical implications of AI?"
# ]

# query ="What are some interesting facts about the history of finance?"
# print(function_call_gem(query))

from google import genai
from google.genai import types
from dotenv import load_dotenv
from os import environ

# Load environment variables
load_dotenv()
genai_key = environ.get("genai_key")

ALL_FUNCTIONS = {
    "tools": [
        {
            "name": "rag_query_resolver",
            "description":"Retrieve factual information from a knowledge base. Use this for questions seeking definitions, explanations, or specific data points.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "query": {"type": "STRING"}
                },
                "required": ["query"]
            }
        },
        {
            "name": "data_analysis",
            "description": "Analyze numerical data. Use this for questions that require calculations, comparisons, or pattern identification within datasets.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "query": {"type": "STRING"}
                },
                "required": ["query"]
            }
        },
        {
            "name": "function_calling",
            "description": "Execute specific functions to retrieve Live market data, News, financial calculations etc. Automate workflows and integrate with external systems.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "query": {"type": "STRING"}
                },
                "required": ["query"]
            }
        },
        {
            "name": "direct_gemini_interaction",
            "description": "Engage in general conversations and access a broad range of internet-accessible information. Use this tool for open-ended queries, explanations, creative writing, and accessing general knowledge that is not specific to financial data. It's suitable for queries where a conversational or exploratory response is desired.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "query": {"type": "STRING"}
                },
                "required": ["query"]
            }
        },
    ]
}

examples = [
    {
        "query": "What is the current price of Apple stock (AAPL)?",
        "function_call": "function_calling",
        "args": { "query": "AAPL" }
    },
    {
        "query": "Who is the CEO of JPMorgan Chase?",
        "function_call": "rag_query_resolver",
        "args": { "query": "JPMorgan Chase CEO" }
    },
    {
        "query": "Analyze the revenue growth of Microsoft (MSFT) over the past 5 years.",
        "function_call": "data_analysis",
        "args": { "query": "Microsoft revenue growth last 5 years" }
    },
    {
        "query": "Get the real-time stock quote for Google (GOOG).",
        "function_call": "function_calling",
        "args": { "query": "GOOG" }
    },
    {
        "query": "What are some interesting facts about the history of finance?",
        "function_call": "direct_gemini_interaction",
        "args": { "query": "history of finance facts" }
    },
    {
        "query": "Compare the profitability of Amazon (AMZN) and Walmart (WMT) based on their operating margins.",
        "function_call": "data_analysis",
        "args": { "query": "Amazon vs Walmart operating margins" }
    },
    {
        "query": "Fetch the latest news headlines related to the Federal Reserve.",
        "function_call": "function_calling",
        "args": { "query": "Federal Reserve latest news" }
    },
    {
        "query": "Summarize the main points of the latest scientific breakthrough.",
        "function_call": "direct_gemini_interaction",
        "args": { "query": "latest scientific breakthrough summary" }
    },
    {
        "query": "Retrieve the historical stock data for Bitcoin (BTC) for the last month.",
        "function_call": "function_calling",
        "args": { "query": "BTC historical data last month" }
    },
    {
        "query": "Explain the key factors influencing the recent inflation rate.",
        "function_call": "rag_query_resolver",
        "args": { "query": "recent inflation rate key factors" }
    },
    {
        "query": "What are the best investment strategies for a volatile market?",
        "function_call": "rag_query_resolver",
        "args": { "query": "best investment strategies for volatility" }
    },
    {
        "query": "Explain the concept of artificial intelligence in simple terms.",
        "function_call": "direct_gemini_interaction",
        "args": { "query": "artificial intelligence explain" }
    }
]

# Configure Gemini client
client = genai.Client(api_key=genai_key)

def function_call_gem(query: str) -> list:
    """
    Calls Gemini AI with the provided query and retrieves function calls.
    """
    client = genai.Client(api_key=genai_key)
    
    # Convert tools into a format Gemini can understand
    config = types.GenerateContentConfig(
        tools=[types.Tool(function_declarations=ALL_FUNCTIONS["tools"])]
    )
    
    try:
        # Include examples in the user prompt.
        example_string = "\n".join([f"Query: {e['query']}\nFunction: {e['function_call']}\nArgs: {e['args']}" for e in examples])
        user_prompt = f"Here are some example queries and their expected function calls. Use these examples to understand the purpose of each function. Do not just match the query to the closest example. Use the function that best fits the users query.\n{example_string}\n\nYour Query: {query}"

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[
                {"role": "user", "parts": [{"text": user_prompt}]}
            ],
            config=config
        )
        return response.function_calls  # Returns the list of function calls
    except Exception as e:
        print(f"Error: {e}")
        return []


random_queries = [
    # rag_query_resolver
    "What is the current yield of the 10-year Treasury bond?",
    "Describe the impact of Brexit on the UK economy.",

    # data_analysis
    "Analyze the correlation between oil prices and airline stock performance.",
    "Compare the financial performance of Coca-Cola (KO) and PepsiCo (PEP).",

    # function_calling
    "What is the current weather forecast for London?",
    "Retrieve the latest stock price for Netflix (NFLX).",

    # direct_gemini_interaction
    "Write a haiku about compound interest.",
    "Summarize the plot of the movie 'Inception'."
]

for query in random_queries:
    print(function_call_gem(query))

