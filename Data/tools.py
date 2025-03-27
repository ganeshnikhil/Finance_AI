TOOL_FUNCTIONS = {
    "tools": [
        {
            "name": "get_news_summary",
            "description": "Fetches recent news articles related to a company using Yahoo Finance and provides a summarized version.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "ticker_symbol": {
                        "type": "STRING",
                        "description": "Stock ticker symbol (e.g., AAPL for Apple)."
                    }
                },
                "required": ["ticker_symbol"]
            }
        },
        {
            "name": "get_stock_overview",
            "description": "Retrieves the latest stock performance overview, including real-time and historical trends.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "ticker_symbol": {
                        "type": "STRING",
                        "description": "Stock ticker symbol (e.g., TSLA for Tesla)."
                    }
                },
                "required": ["ticker_symbol"]
            }
        }
    ]
}


TOOL_FUNCTION_EXAMPLES = [
    {
        "query": "Summarize the latest news related to Apple (AAPL).",
        "function_call": "get_news_summary",
        "args": {
            "ticker_symbol": "AAPL"
        }
    },
    {
        "query": "Fetch key news highlights for Tesla (TSLA).",
        "function_call": "get_news_summary",
        "args": {
            "ticker_symbol": "TSLA"
        }
    },
    {
        "query": "Get a financial overview of Google with historical trends.",
        "function_call": "get_stock_overview",
        "args": {
            "ticker_symbol": "GOOGL"
        }
    },
    {
        "query": "Show the recent financial trends of Microsoft.",
        "function_call": "get_stock_overview",
        "args": {
            "ticker_symbol": "MSFT"
        }
    },
    {
        "query": "Summarize the recent news articles related to Amazon.",
        "function_call": "get_news_summary",
        "args": {
            "ticker_symbol": "AMZN"
        }
    },
    {
        "query": "Analyze the financial updates of Netflix (NFLX) with price movements.",
        "function_call": "get_stock_overview",
        "args": {
            "ticker_symbol": "NFLX"
        }
    },
    {
        "query": "Summarize recent highlights for Meta Platforms (META).",
        "function_call": "get_news_summary",
        "args": {
            "ticker_symbol": "META"
        }
    },
    {
        "query": "Fetch performance insights about Reliance Industries (RELIANCE.NS).",
        "function_call": "get_stock_overview",
        "args": {
            "ticker_symbol": "RELIANCE.NS"
        }
    },
    {
        "query": "Summarize the latest news trends of Tata Consultancy Services (TCS.NS).",
        "function_call": "get_news_summary",
        "args": {
            "ticker_symbol": "TCS.NS"
        }
    },
    {
        "query": "Get a detailed financial overview of Infosys (INFY.NS).",
        "function_call": "get_stock_overview",
        "args": {
            "ticker_symbol": "INFY.NS"
        }
    }
]


ROUTING_MAP_FUNCTIONS = {
    "tools": [
        {
            "name": "rag_query_resolver",
            "description": "Retrieve factual information from a knowledge base. Use this for questions seeking definitions, explanations, or specific data points.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "query": {
                        "type": "STRING",
                        "description": "The query to retrieve factual data."
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "data_analysis",
            "description": "Analyze numerical data. Use this for questions that require calculations, comparisons, or identifying patterns within datasets.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "query": {
                        "type": "STRING",
                        "description": "The query for data analysis tasks."
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "function_calling",
            "description": "Execute specific functions to retrieve real-time financial data, stock quotes, market news, and economic indicators.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "query": {
                        "type": "STRING",
                        "description": "The query to execute a relevant function."
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "direct_gemini_interaction",
            "description": "Engage in general conversations and access a broad range of internet-accessible information. Use this tool for open-ended queries, explanations, and creative tasks.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "query": {
                        "type": "STRING",
                        "description": "The query for general conversation or information retrieval."
                    }
                },
                "required": ["query"]
            }
        }
    ]
}

ROUTING_MAP_EXAMPLES = [
    {
        "query": "What is the current price of Apple stock (AAPL)?",
        "function_call": "function_calling",
        "args": {
            "query": "current price of Apple stock (AAPL)"
        }
    },
    {
        "query": "Who is the CEO of JPMorgan Chase?",
        "function_call": "direct_gemini_interaction",
        "args": {
            "query": "CEO of JPMorgan Chase"
        }
    },
    {
        "query": "Analyze the revenue growth of Microsoft (MSFT) over the past 5 years.",
        "function_call": "data_analysis",
        "args": {
            "query": "Microsoft revenue growth last 5 years"
        }
    },
    {
        "query": "Get the real-time stock quote for Google (GOOG).",
        "function_call": "function_calling",
        "args": {
            "query": "stock quote for Google (GOOG)"
        }
    },
    {
        "query": "What are some interesting facts about the history of finance?",
        "function_call": "rag_query_resolver",
        "args": {
            "query": "history of finance facts"
        }
    },
    {
        "query": "Compare the profitability of Amazon (AMZN) and Walmart (WMT) based on operating margins.",
        "function_call": "data_analysis",
        "args": {
            "query": "Amazon (AMZN) vs Walmart (WMT) operating margins"
        }
    },
    {
        "query": "Fetch the latest news headlines related to the Federal Reserve.",
        "function_call": "function_calling",
        "args": {
            "query": "Federal Reserve latest news"
        }
    },
    {
        "query": "Summarize the main points of the latest scientific breakthrough.",
        "function_call": "direct_gemini_interaction",
        "args": {
            "query": "latest scientific breakthrough summary"
        }
    },
    {
        "query": "Explain the key factors influencing the recent inflation rate.",
        "function_call": "direct_gemini_interaction",
        "args": {
            "query": "recent inflation rate key factors"
        }
    },
    {
        "query": "What are the best investment strategies for a volatile market?",
        "function_call": "rag_query_resolver",
        "args": {
            "query": "best investment strategies for volatility"
        }
    },
    {
        "query": "Explain the concept of artificial intelligence in simple terms.",
        "function_call": "direct_gemini_interaction",
        "args": {
            "query": "artificial intelligence explain"
        }
    },
    {
        "query": "Get the most recent press release from Tesla.",
        "function_call": "function_calling",
        "args": {
            "query": "Tesla press release"
        }
    },
    {
        "query": "What is the definition of a stock split?",
        "function_call": "rag_query_resolver",
        "args": {
            "query": "stock split definition"
        }
    }
]
