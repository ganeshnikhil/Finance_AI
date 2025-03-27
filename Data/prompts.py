

# structured_prompt = {
#     "task": "Your task is to generate a perfect SQL query to retrieve the necessary data from a database to answer the user's question.",
#     "instructions": [
#         "The user will pose a question about a company's financial performance or stock-related details.",
#         "Analyze the question thoroughly to identify the specific financial metrics or data points being requested.",
#         "Use only the provided table name and columns to generate the SQL query.",
#         "The SQL query must retrieve only the necessary columns and filter the data based on conditions explicitly mentioned in the user's question (e.g., year, company name, or specific metrics).",
#         "Include a LIMIT clause (e.g., LIMIT 10) if no specific filtering condition is mentioned in the user's question",
#         "Ensure the query is syntactically correct and fetches only the required data from the database.",
#         "If the table name is provided as a list of company names, dynamically select the table corresponding to the company mentioned in the user's question.",
#         "Do not attempt to solve or explain the query, only generate the SQL query for retrieving relevant data."
#     ],
#     "input_format": {
#         "table_names": ["array of company names"],
#         "columns": ["array of shared column names"],
#         "user_question": "string"
#     },
#     "output_format": {
#         "sql_query": "string",
#         "clarification_note": "string (optional, include only if needed)"
#     }
# }

# question = {
#     "table_names":["reliance", "aapl", "fb", "googl", "tsla"],
#     "columns":['year', 'Tax Effect Of Unusual Items', 'Tax Rate For Calcs', 'Normalized EBITDA', 'Net Income From Continuing Operation Net Minority Interest', 'Reconciled Depreciation', 
#             'Reconciled Cost Of Revenue', 'EBITDA', 'EBIT', 'Net Interest Income', 'Interest Expense', 'Interest Income', 
#             'Normalized Income', 'Net Income From Continuing And Discontinued Operation', 'Total Expenses', 'Total Operating Income As Reported', 
#             'Diluted Average Shares', 'Basic Average Shares', 'Diluted EPS', 'Basic EPS', 'Diluted NI Availto Com Stockholders', 'Net Income Common Stockholders', 'Net Income', 
#             'Net Income Including Noncontrolling Interests', 'Net Income Continuous Operations', 'Tax Provision', 'Pretax Income', 'Other Income Expense', 'Other Non Operating Income Expenses', 
#             'Net Non Operating Interest Income Expense', 'Interest Expense Non Operating', 'Interest Income Non Operating', 'Operating Income', 'Operating Expense', 'Research And Development', 'Selling General And Administration', 
#             'Gross Profit', 'Cost Of Revenue', 'Total Revenue', 'Operating Revenue', 'Treasury Shares Number', 'Ordinary Shares Number', 'Share Issued', 'Net Debt', 'Total Debt', 'Tangible Book Value', 
#             'Invested Capital', 'Working Capital', 'Net Tangible Assets', 'Capital Lease Obligations', 'Common Stock Equity', 'Total Capitalization', 
#             'Total Equity Gross Minority Interest', 'Stockholders Equity', 'Gains Losses Not Affecting Retained Earnings', 'Other Equity Adjustments', 
#             'Retained Earnings', 'Capital Stock', 'Common Stock', 'Total Liabilities Net Minority Interest', 'Total Non Current Liabilities Net Minority Interest', 'Other Non Current Liabilities', 
#             'Tradeand Other Payables Non Current', 'Long Term Debt And Capital Lease Obligation', 'Long Term Capital Lease Obligation', 'Long Term Debt', 'Current Liabilities', 'Other Current Liabilities', 
#             'Current Deferred Liabilities', 'Current Deferred Revenue', 'Current Debt And Capital Lease Obligation', 'Current Capital Lease Obligation', 'Current Debt', 
#             'Other Current Borrowings', 'Commercial Paper', 'Payables And Accrued Expenses', 'Payables', 'Total Tax Payable', 'Income Tax Payable', 'Accounts Payable', 'Total Assets', 'Total Non Current Assets', 
#             'Other Non Current Assets', 'Non Current Deferred Assets', 'Non Current Deferred Taxes Assets', 'Investments And Advances', 'Other Investments', 'Investmentin Financial Assets', 'Available For Sale Securities', 
#             'Net PPE', 'Accumulated Depreciation', 'Gross PPE', 'Leases', 'Other Properties', 'Machinery Furniture Equipment', 'Land And Improvements', 'Properties', 'Current Assets', 'Other Current Assets', 'Inventory', 
#             'Receivables', 'Other Receivables', 'Accounts Receivable', 'Cash Cash Equivalents And Short Term Investments', 'Other Short Term Investments', 'Cash And Cash Equivalents', 'Cash Equivalents', 'Cash Financial', 
#             'Free Cash Flow', 'Repurchase Of Capital Stock', 'Repayment Of Debt', 'Issuance Of Debt', 'Issuance Of Capital Stock', 'Capital Expenditure', 'Interest Paid Supplemental Data', 'Income Tax Paid Supplemental Data', 'End Cash Position', 'Beginning Cash Position',
#             'Changes In Cash', 'Financing Cash Flow', 'Cash Flow From Continuing Financing Activities', 'Net Other Financing Charges', 'Cash Dividends Paid', 'Common Stock Dividend Paid', 'Net Common Stock Issuance', 'Common Stock Payments', 
#             'Common Stock Issuance', 'Net Issuance Payments Of Debt', 'Net Short Term Debt Issuance', 'Net Long Term Debt Issuance', 'Long Term Debt Payments', 'Long Term Debt Issuance', 
#             'Investing Cash Flow', 'Cash Flow From Continuing Investing Activities', 'Net Other Investing Changes', 'Net Investment Purchase And Sale', 'Sale Of Investment', 'Purchase Of Investment', 
#             'Net Business Purchase And Sale', 'Purchase Of Business', 'Net PPE Purchase And Sale', 'Purchase Of PPE', 'Operating Cash Flow', 'Cash Flow From Continuing Operating Activities', 'Change In Working Capital', 
#             'Change In Other Working Capital', 'Change In Other Current Liabilities', 'Change In Other Current Assets', 'Change In Payables And Accrued Expense', 'Change In Payable', 'Change In Account Payable', 'Change In Inventory', 
#             'Change In Receivables', 'Changes In Account Receivables', 'Other Non Cash Items', 'Stock Based Compensation', 'Deferred Tax', 'Deferred Income Tax', 'Depreciation Amortization Depletion', 'Depreciation And Amortization',
#             'Net Income From Continuing Operations', 'period_category'],
#     "user_question":""
# }

# [
#         "symbol",
#         "profit",
#         "loss",
#         "year",
#         "Stock Price",
#         "Total Shares Outstanding",
#         "Promoter Holding",
#         "Market Capitalization",
#         "Earnings Per Share",
#         "Book Value",
#         "Dividends",
#         "Deliverables (%)",
#         "cashflow",
#         "PE ratio"
#     ]


# structured_prompt = {
#     "task": "Your task is to generate a perfect SQL query to retrieve the necessary data from a database to answer the user's question.",
#     "instructions": [
#         "The user will pose a question about a company's annual financial performance or stock-related details.",
#         "Analyze the question thoroughly to identify the specific financial metrics or data points being requested.",
#         "Use only the provided table names (company names) and columns to generate the SQL query.",
#         "The data spans from 2020 to 2024 and is annual only. Ensure the query filters the 'year' column appropriately if the user specifies a time range.",
#         "Some fields in the columns may contain NULL values. Handle NULL values appropriately by including IS NOT NULL in filtering conditions if relevant to the question.",
#         "Include a LIMIT clause (e.g., LIMIT 10) if no specific filtering condition is mentioned in the user's question.",
#         "If the user does not specify a particular company, retrieve data from all company tables provided in the 'table_names' input.",
#         "Ensure the SQL query is syntactically correct and fetches only the required data from the database.",
#         "If the table name is provided as a list of company names, dynamically select the table corresponding to the company mentioned in the user's question.",
#         "Do not attempt to solve or explain the query, only generate the SQL query for retrieving relevant data."
#     ],
#     "input_format": {
#         "table_names": ["array of company names"],
#         "columns": ["array of shared column names"],
#         "user_question": "string"
#     },
#     "additional_context": {
#         "data_info": {
#             "time_range": "2020 to 2024",
#             "frequency": "Annual only",
#             "null_handling": "Some fields may contain NULL values.",
#             "primary_columns": ["year", "period_category"]
#         }
#     },
#     "output_format": {
#         "sql_query": "string",
#         "clarification_note": "string (optional, include only if needed)"
#     }
# }




# question = {
#     "table_names":["reliance", "aapl", "fb", "googl", "tsla"],
#     "columns":['year', 'Tax Effect Of Unusual Items', 'Tax Rate For Calcs', 'Normalized EBITDA', 'Net Income From Continuing Operation Net Minority Interest', 'Reconciled Depreciation', 
#             'Reconciled Cost Of Revenue', 'EBITDA', 'EBIT', 'Net Interest Income', 'Interest Expense', 'Interest Income', 
#             'Normalized Income', 'Net Income From Continuing And Discontinued Operation', 'Total Expenses', 'Total Operating Income As Reported', 
#             'Diluted Average Shares', 'Basic Average Shares', 'Diluted EPS', 'Basic EPS', 'Diluted NI Availto Com Stockholders', 'Net Income Common Stockholders', 'Net Income', 
#             'Net Income Including Noncontrolling Interests', 'Net Income Continuous Operations', 'Tax Provision', 'Pretax Income', 'Other Income Expense', 'Other Non Operating Income Expenses', 
#             'Net Non Operating Interest Income Expense', 'Interest Expense Non Operating', 'Interest Income Non Operating', 'Operating Income', 'Operating Expense', 'Research And Development', 'Selling General And Administration', 
#             'Gross Profit', 'Cost Of Revenue', 'Total Revenue', 'Operating Revenue', 'Treasury Shares Number', 'Ordinary Shares Number', 'Share Issued', 'Net Debt', 'Total Debt', 'Tangible Book Value', 
#             'Invested Capital', 'Working Capital', 'Net Tangible Assets', 'Capital Lease Obligations', 'Common Stock Equity', 'Total Capitalization', 
#             'Total Equity Gross Minority Interest', 'Stockholders Equity', 'Gains Losses Not Affecting Retained Earnings', 'Other Equity Adjustments', 
#             'Retained Earnings', 'Capital Stock', 'Common Stock', 'Total Liabilities Net Minority Interest', 'Total Non Current Liabilities Net Minority Interest', 'Other Non Current Liabilities', 
#             'Tradeand Other Payables Non Current', 'Long Term Debt And Capital Lease Obligation', 'Long Term Capital Lease Obligation', 'Long Term Debt', 'Current Liabilities', 'Other Current Liabilities', 
#             'Current Deferred Liabilities', 'Current Deferred Revenue', 'Current Debt And Capital Lease Obligation', 'Current Capital Lease Obligation', 'Current Debt', 
#             'Other Current Borrowings', 'Commercial Paper', 'Payables And Accrued Expenses', 'Payables', 'Total Tax Payable', 'Income Tax Payable', 'Accounts Payable', 'Total Assets', 'Total Non Current Assets', 
#             'Other Non Current Assets', 'Non Current Deferred Assets', 'Non Current Deferred Taxes Assets', 'Investments And Advances', 'Other Investments', 'Investmentin Financial Assets', 'Available For Sale Securities', 
#             'Net PPE', 'Accumulated Depreciation', 'Gross PPE', 'Leases', 'Other Properties', 'Machinery Furniture Equipment', 'Land And Improvements', 'Properties', 'Current Assets', 'Other Current Assets', 'Inventory', 
#             'Receivables', 'Other Receivables', 'Accounts Receivable', 'Cash Cash Equivalents And Short Term Investments', 'Other Short Term Investments', 'Cash And Cash Equivalents', 'Cash Equivalents', 'Cash Financial', 
#             'Free Cash Flow', 'Repurchase Of Capital Stock', 'Repayment Of Debt', 'Issuance Of Debt', 'Issuance Of Capital Stock', 'Capital Expenditure', 'Interest Paid Supplemental Data', 'Income Tax Paid Supplemental Data', 'End Cash Position', 'Beginning Cash Position',
#             'Changes In Cash', 'Financing Cash Flow', 'Cash Flow From Continuing Financing Activities', 'Net Other Financing Charges', 'Cash Dividends Paid', 'Common Stock Dividend Paid', 'Net Common Stock Issuance', 'Common Stock Payments', 
#             'Common Stock Issuance', 'Net Issuance Payments Of Debt', 'Net Short Term Debt Issuance', 'Net Long Term Debt Issuance', 'Long Term Debt Payments', 'Long Term Debt Issuance', 
#             'Investing Cash Flow', 'Cash Flow From Continuing Investing Activities', 'Net Other Investing Changes', 'Net Investment Purchase And Sale', 'Sale Of Investment', 'Purchase Of Investment', 
#             'Net Business Purchase And Sale', 'Purchase Of Business', 'Net PPE Purchase And Sale', 'Purchase Of PPE', 'Operating Cash Flow', 'Cash Flow From Continuing Operating Activities', 'Change In Working Capital', 
#             'Change In Other Working Capital', 'Change In Other Current Liabilities', 'Change In Other Current Assets', 'Change In Payables And Accrued Expense', 'Change In Payable', 'Change In Account Payable', 'Change In Inventory', 
#             'Change In Receivables', 'Changes In Account Receivables', 'Other Non Cash Items', 'Stock Based Compensation', 'Deferred Tax', 'Deferred Income Tax', 'Depreciation Amortization Depletion', 'Depreciation And Amortization',
#             'Net Income From Continuing Operations', 'period_category'],
#     "user_question":""
# }



structured_prompt = {
    "task": "Your task is to decide whether to generate an SQL query to retrieve data from a database or a function call to fulfill the user's request.",
    "instructions": [
        "The user will pose a question that may involve querying data from a database or requiring a function call for additional processing.",
        "Analyze the user's question to determine whether the request pertains to database queries or a specific function call.",
        "For database queries:",
        "  - Use only the provided table names and columns to generate the SQL query.",
        "  - Include conditions to filter the data appropriately based on the user's question (e.g., year, company, metrics).",
        "  - If the user specifies a time range, filter the 'year' column accordingly.",
        "  - Handle NULL values appropriately by including IS NOT NULL in filtering conditions if relevant.",
        "  - If no filtering condition is specified, include a LIMIT clause (e.g., LIMIT 10).",
        "  - If the user does not specify a particular table, retrieve data from all the provided table names.",
        "  - Use aggregate functions (e.g., SUM, AVG) for mathematical operations if required.",
        "For function calls:",
        "  - Use the provided list of functions to generate the appropriate function call.",
        "  - Ensure the function call dynamically matches the user's intent (e.g., fetching data, computing metrics, retrieving news, or other operations).",
        "  - Include necessary arguments for the function, such as company symbols, date ranges, or other parameters relevant to the user's question.",
        "Ensure the output explicitly specifies whether it is an SQL query or a function call, along with the generated query or function."
    ],
    "input_format": {
        "query_type": "string (either 'database_query' or 'function_call')",
        "table_names": ["array of table names (for database queries)"],
        "columns": ["array of shared column names (for database queries)"],
        "functions": ["array of function names with their descriptions (e.g., 'fetch_latest_news' for retrieving news, 'calculate_metrics' for computing metrics)"],
        "user_question": "string"
    },
    "additional_context": {
        "database_info": {
            "time_range": "2020 to 2024",
            "frequency": "Annual data only",
            "limitations": "Quarterly/monthly data unavailable. Use 'year' for filtering.",
            "row_structure": "Each row represents the data for a single year per company.",
            "primary_columns": ["year", "period_category"]
        },
        "function_info": {
            "usage": "Dynamically construct a function call based on the user's query.",
            "priority": "Prioritize dynamic parameter mapping (e.g., 'TSLA' for Tesla).",
            "arguments": "Pass arguments dynamically based on the user's question (e.g., symbol, start_date, metrics)."
        }
    },
    "output_format": {
        "sql_query": {
            "required": "boolean (true if an SQL query is needed, false otherwise)",
            "query": "string (SQL query to retrieve the required data, if applicable)",
            "clarification_note": "string (optional, include only if clarification about the SQL query is needed)"
        },
        "function_call": {
            "required": "boolean (true if a function call is needed, false otherwise)",
            "call": {
                "name": "string (function name)",
                "parameters": "object (key-value pairs of arguments)"
            },
            "clarification_note": "string (optional, include only if clarification about the function call is needed)"
        }
    },
    "examples":[
    {
        "user_question": "What was Apple’s revenue in 2022?",
        "output": {"sql_query": {"required": True, "query": "SELECT year, Total_Revenue FROM aapl WHERE year = 2022"}}
    },
    {
        "user_question": "Fetch latest news about Tesla",
        "output": {"function_call": {"required": True, "call": {"name": "stock_news", "parameters": {"Symbol": "TSLA"}}}}
    }
    ]
}



question = {
    "table_names":["reliance", "aapl", "fb", "googl", "tsla"],
    "columns":['year', 'Tax Effect Of Unusual Items', 'Tax Rate For Calcs', 'Normalized EBITDA', 'Net Income From Continuing Operation Net Minority Interest', 'Reconciled Depreciation', 
            'Reconciled Cost Of Revenue', 'EBITDA', 'EBIT', 'Net Interest Income', 'Interest Expense', 'Interest Income', 
            'Normalized Income', 'Net Income From Continuing And Discontinued Operation', 'Total Expenses', 'Total Operating Income As Reported', 
            'Diluted Average Shares', 'Basic Average Shares', 'Diluted EPS', 'Basic EPS', 'Diluted NI Availto Com Stockholders', 'Net Income Common Stockholders', 'Net Income', 
            'Net Income Including Noncontrolling Interests', 'Net Income Continuous Operations', 'Tax Provision', 'Pretax Income', 'Other Income Expense', 'Other Non Operating Income Expenses', 
            'Net Non Operating Interest Income Expense', 'Interest Expense Non Operating', 'Interest Income Non Operating', 'Operating Income', 'Operating Expense', 'Research And Development', 'Selling General And Administration', 
            'Gross Profit', 'Cost Of Revenue', 'Total Revenue', 'Operating Revenue', 'Treasury Shares Number', 'Ordinary Shares Number', 'Share Issued', 'Net Debt', 'Total Debt', 'Tangible Book Value', 
            'Invested Capital', 'Working Capital', 'Net Tangible Assets', 'Capital Lease Obligations', 'Common Stock Equity', 'Total Capitalization', 
            'Total Equity Gross Minority Interest', 'Stockholders Equity', 'Gains Losses Not Affecting Retained Earnings', 'Other Equity Adjustments', 
            'Retained Earnings', 'Capital Stock', 'Common Stock', 'Total Liabilities Net Minority Interest', 'Total Non Current Liabilities Net Minority Interest', 'Other Non Current Liabilities', 
            'Tradeand Other Payables Non Current', 'Long Term Debt And Capital Lease Obligation', 'Long Term Capital Lease Obligation', 'Long Term Debt', 'Current Liabilities', 'Other Current Liabilities', 
            'Current Deferred Liabilities', 'Current Deferred Revenue', 'Current Debt And Capital Lease Obligation', 'Current Capital Lease Obligation', 'Current Debt', 
            'Other Current Borrowings', 'Commercial Paper', 'Payables And Accrued Expenses', 'Payables', 'Total Tax Payable', 'Income Tax Payable', 'Accounts Payable', 'Total Assets', 'Total Non Current Assets', 
            'Other Non Current Assets', 'Non Current Deferred Assets', 'Non Current Deferred Taxes Assets', 'Investments And Advances', 'Other Investments', 'Investmentin Financial Assets', 'Available For Sale Securities', 
            'Net PPE', 'Accumulated Depreciation', 'Gross PPE', 'Leases', 'Other Properties', 'Machinery Furniture Equipment', 'Land And Improvements', 'Properties', 'Current Assets', 'Other Current Assets', 'Inventory', 
            'Receivables', 'Other Receivables', 'Accounts Receivable', 'Cash Cash Equivalents And Short Term Investments', 'Other Short Term Investments', 'Cash And Cash Equivalents', 'Cash Equivalents', 'Cash Financial', 
            'Free Cash Flow', 'Repurchase Of Capital Stock', 'Repayment Of Debt', 'Issuance Of Debt', 'Issuance Of Capital Stock', 'Capital Expenditure', 'Interest Paid Supplemental Data', 'Income Tax Paid Supplemental Data', 'End Cash Position', 'Beginning Cash Position',
            'Changes In Cash', 'Financing Cash Flow', 'Cash Flow From Continuing Financing Activities', 'Net Other Financing Charges', 'Cash Dividends Paid', 'Common Stock Dividend Paid', 'Net Common Stock Issuance', 'Common Stock Payments', 
            'Common Stock Issuance', 'Net Issuance Payments Of Debt', 'Net Short Term Debt Issuance', 'Net Long Term Debt Issuance', 'Long Term Debt Payments', 'Long Term Debt Issuance', 
            'Investing Cash Flow', 'Cash Flow From Continuing Investing Activities', 'Net Other Investing Changes', 'Net Investment Purchase And Sale', 'Sale Of Investment', 'Purchase Of Investment', 
            'Net Business Purchase And Sale', 'Purchase Of Business', 'Net PPE Purchase And Sale', 'Purchase Of PPE', 'Operating Cash Flow', 'Cash Flow From Continuing Operating Activities', 'Change In Working Capital', 
            'Change In Other Working Capital', 'Change In Other Current Liabilities', 'Change In Other Current Assets', 'Change In Payables And Accrued Expense', 'Change In Payable', 'Change In Account Payable', 'Change In Inventory', 
            'Change In Receivables', 'Changes In Account Receivables', 'Other Non Cash Items', 'Stock Based Compensation', 'Deferred Tax', 'Deferred Income Tax', 'Depreciation Amortization Depletion', 'Depreciation And Amortization',
            'Net Income From Continuing Operations', 'period_category'],
    "functions": [
        {
            "name": "stock_news",
            "description": "Get the latest Financial news",
            "parameters": {
                "Symbol": "string",
                "required": ["Symbol"]
            }
        },
    ],
    "user_question":""
}