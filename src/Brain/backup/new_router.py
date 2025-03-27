# from google import genai
# from google.genai import types
# from dotenv import load_dotenv
# from os import environ
# import re
# import json
# from datetime import datetime

# # Load environment variables
# load_dotenv()
# genai_key = environ.get("genai_key")

# ALL_FUNCTIONS = {
#     "tools": [
#         {
#             "name": "rag_query_resolver",
#             "description": "Retrieve precise financial information from a knowledge base. ONLY USE for specific questions about market data, company facts, economic indicators, financial definitions, or industry statistics. DO NOT USE for analysis, calculations, real-time data, or general conversations.",
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
#             "description": "Perform analysis on stored financial datasets. ONLY USE when asked to analyze, compare, find patterns, or generate insights from existing financial data. DO NOT USE for retrieving current prices, news, executing calculations, or general information.",
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
#             "description": "Execute external API calls for live data or calculations. ONLY USE for real-time market data, current prices, news retrieval, currency conversion, or financial calculations. DO NOT USE for historical analysis, general knowledge, or conversation.",
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
#             "description": "Handle general knowledge and conversational queries. ONLY USE for general information, explanations, creative content, or topics outside of specific financial data, analysis, or real-time information.",
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

# # Pre-process query to suggest the most appropriate tool
# def suggest_tool(query):
#     query = query.lower()
    
#     # Define pattern matching for each tool
#     rag_patterns = [
#         r"what is the .*(price|value|worth) of .*\b(stock|share)\b",
#         r"\b(what|who|when|where|explain|provide|summary)\b.*\b(is|are|was|were)\b",
#         r"\b(difference|between|definition)\b"
#     ]
    
#     analysis_patterns = [
#         r"\b(analyze|analysis|compare|trend|calculate average|top|performance)\b",
#         r"\b(growth|ratio|margin|profitability)\b.*(over|past|last|years|quarters)\b",
#         r"\b(statistics|correlation|regression|forecast)\b"
#     ]
    
#     function_patterns = [
#         r"\b(real-time|live|current|today|now|latest)\b",
#         r"\b(calculate|compute|convert)\b",
#         r"\b(fetch|get|retrieve)\b.*\b(news|data)\b"
#     ]
    
#     # Check patterns
#     for pattern in rag_patterns:
#         if re.search(pattern, query):
#             return "rag_query_resolver"
            
#     for pattern in analysis_patterns:
#         if re.search(pattern, query):
#             return "data_analysis"
            
#     for pattern in function_patterns:
#         if re.search(pattern, query):
#             return "function_calling"
    
#     # Default to direct interaction if no specific pattern matches
#     return "direct_gemini_interaction"

# def is_critical_mismatch(suggested, selected, query):
#     """
#     Determine if a mismatch between suggested and selected tools is critical.
#     Returns True if the mismatch is critical and should be overridden.
#     """
#     # Critical case 1: Specific financial data should not use direct_gemini_interaction
#     if suggested in ["rag_query_resolver", "function_calling"] and selected == "direct_gemini_interaction":
#         if re.search(r"\b(price|stock|market|rate|percentage|calculate|earnings|CEO|GDP)\b", query.lower()):
#             return True
    
#     # Critical case 2: Analysis queries should not use rag_query_resolver
#     if suggested == "data_analysis" and selected == "rag_query_resolver":
#         if re.search(r"\b(analyze|trend|growth|compare|ratio|over|past|performance)\b", query.lower()):
#             return True
    
#     # Critical case 3: Live data should use function_calling
#     if suggested == "function_calling" and selected != "function_calling":
#         if re.search(r"\b(real-time|current|latest|today|now|live)\b", query.lower()):
#             return True
    
#     # Non-critical cases
#     return False

# def log_mismatch(suggested_tool, selected_tool, query, outcome):
#     """Log mismatches for later analysis and improvement"""
#     try:
#         with open("tool_mismatch_log.jsonl", "a") as f:
#             f.write(json.dumps({
#                 "timestamp": datetime.now().isoformat(),
#                 "query": query,
#                 "suggested_tool": suggested_tool,
#                 "selected_tool": selected_tool,
#                 "outcome": outcome
#             }) + "\n")
#     except Exception as e:
#         print(f"Failed to log mismatch: {e}")

# def process_with_tool(tool_name, query_text):
#     """
#     Mock function to process a query with a specific tool.
#     In a real implementation, this would call the appropriate service.
#     """
#     # This is a placeholder - in a real system, you would route to the actual tool implementation
#     print(f"Processing with {tool_name}: {query_text}")
#     return {"tool": tool_name, "query": query_text, "status": "processed"}

# def validate_result(tool_name, result):
#     """
#     Validate the result from a tool to detect hallucinations or errors.
#     Returns True if the result seems valid, False otherwise.
#     """
#     # This is a placeholder - in a real system, you would implement actual validation logic
#     # such as checking for specific data patterns, consistency, etc.
    
#     # For example:
#     if tool_name == "rag_query_resolver" and "specific_data" not in result:
#         return False
#     if tool_name == "function_calling" and "api_response" not in result:
#         return False
    
#     # Default to assuming valid for this demo - change this in production
#     return True

# # Helper function to convert function calls to serializable format
# def serialize_function_calls(function_calls):
#     """Convert function call objects to serializable dictionaries"""
#     if not function_calls:
#         return []
        
#     serialized = []
#     for fc in function_calls:
#         # Extract only the data we need in a serializable format
#         serialized_call = {
#             "name": fc.name,
#             "args": fc.args if hasattr(fc, 'args') else {}
#         }
#         serialized.append(serialized_call)
    
#     return serialized

# def function_call_gem(query: str) -> dict:
#     """
#     Calls Gemini AI with the provided query and retrieves function calls with improved precision.
#     Returns a dictionary with the function call results and metadata.
#     """
#     client = genai.Client(api_key=genai_key)
    
#     # Pre-process query to determine most likely tool
#     suggested_tool = suggest_tool(query)
    
#     # Add guidance to the query to help Gemini select the right tool
#     enhanced_query = f"""
#     Query: {query}
    
#     Based on the nature of this query, the most appropriate tool to use would likely be '{suggested_tool}'.
#     Please prioritize accuracy and only return information you're confident about.
#     """
    
#     # Configure Gemini
#     config = types.GenerateContentConfig(
#         tools=[types.Tool(function_declarations=ALL_FUNCTIONS["tools"])]
#     )
    
#     try:
#         response = client.models.generate_content(
#             model='gemini-2.0-flash',
#             contents=enhanced_query,
#             config=config
#         )
        
#         # Extract function calls
#         function_calls = response.function_calls if hasattr(response, 'function_calls') else []
        
#         if not function_calls:
#             print("Warning: No function calls returned")
#             fallback_result = {
#                 "status": "fallback",
#                 "tool": suggested_tool,
#                 "query": query,
#                 "message": "No function calls returned by Gemini"
#             }
#             return fallback_result
        
#         selected_tool = function_calls[0].name if function_calls else suggested_tool
        
#         # Check if Gemini selected the suggested tool
#         if selected_tool != suggested_tool:
#             print(f"Mismatch: Gemini selected {selected_tool} instead of suggested {suggested_tool}")
            
#             # Check if this is a critical mismatch
#             if is_critical_mismatch(suggested_tool, selected_tool, query):
#                 print(f"Critical mismatch detected: overriding {selected_tool} with {suggested_tool}")
                
#                 # Log the override
#                 log_mismatch(suggested_tool, selected_tool, query, "override")
                
#                 # Use the suggested tool instead
#                 final_tool = suggested_tool
#             else:
#                 print(f"Non-critical mismatch: proceeding with Gemini's selection of {selected_tool}")
                
#                 # Log the acceptance
#                 log_mismatch(suggested_tool, selected_tool, query, "accepted")
                
#                 # Use Gemini's selection
#                 final_tool = selected_tool
#         else:
#             # Suggested and selected tools match
#             final_tool = selected_tool
        
#         # Execute the query with the final tool selection
#         result = process_with_tool(final_tool, query)
        
#         # For demo purposes, add mock data for validation
#         if final_tool == "rag_query_resolver":
#             result["specific_data"] = {"found": True, "source": "financial database"}
#         elif final_tool == "function_calling":
#             result["api_response"] = {"status": "success", "data": {"price": 150.25}}
        
#         # Validate the result
#         if not validate_result(final_tool, result):
#             print(f"Warning: Result validation failed for {final_tool}")
            
#             # If Gemini's selection failed validation and it was different from our suggestion,
#             # try the suggested tool as a fallback
#             if final_tool != suggested_tool:
#                 print(f"Trying suggested tool {suggested_tool} as fallback")
#                 result = process_with_tool(suggested_tool, query)
                
#                 # Add mock data for validation of the fallback
#                 if suggested_tool == "rag_query_resolver":
#                     result["specific_data"] = {"found": True, "source": "financial database"}
#                 elif suggested_tool == "function_calling":
#                     result["api_response"] = {"status": "success", "data": {"price": 150.25}}
                
#                 # If the fallback also fails validation, log this critical failure
#                 if not validate_result(suggested_tool, result):
#                     print("Critical: Both tool selections failed validation")
#                     log_mismatch(suggested_tool, selected_tool, query, "both_failed_validation")
#                 else:
#                     log_mismatch(suggested_tool, selected_tool, query, "fallback_succeeded")
#                     final_tool = suggested_tool
#             else:
#                 log_mismatch(suggested_tool, selected_tool, query, "validation_failed")
        
#         # Return the final result with metadata, making sure everything is serializable
#         return {
#             "status": "success",
#             "original_query": query,
#             "suggested_tool": suggested_tool,
#             "selected_tool": selected_tool,
#             "final_tool": final_tool,
#             "function_calls": serialize_function_calls(function_calls),
#             "result": result
#         }
        
#     except Exception as e:
#         print(f"Error in function_call_gem: {e}")
        
#         # Return error information
#         error_result = {
#             "status": "error",
#             "tool": suggested_tool,  # Fall back to the suggested tool
#             "query": query,
#             "error": str(e)
#         }
        
#         return error_result

# # Example usage
# def main():
#     # Test with different query types
#     queries = [
#         # RAG queries
#         "What is the current price of Apple stock (AAPL)?",
#         "Who is the CEO of JPMorgan Chase?",
        
#         # Analysis queries
#         "Analyze the revenue growth of Microsoft over the past 5 years.",
#         "Compare the profitability of Amazon and Walmart.",
        
#         # Function calling queries
#         "Get the real-time stock quote for Google.",
#         "Calculate the present value of $10,000 in 5 years at 6% interest.",
        
#         # Direct interaction queries
#         "What are some interesting facts about the history of finance?",
#         "Write a short poem about the stock market."
#     ]
    
#     for idx, query in enumerate(queries):
#         print(f"\n=== Test Query {idx+1}: {query} ===")
#         result = function_call_gem(query)
        
#         # Ensure result is serializable before printing
#         print(f"Result: {json.dumps(result, indent=2)}")

# if __name__ == "__main__":
#     main()


from google import genai
from google.genai import types
from dotenv import load_dotenv
from os import environ
import re
import json
from datetime import datetime

# Load environment variables
load_dotenv()
genai_key = environ.get("genai_key")

ALL_FUNCTIONS = {
    "tools": [
        {
            "name": "rag_query_resolver",
            "description": "Retrieve precise financial information from a knowledge base. Use this for market data, company facts, economic indicators, or industry statistics.",
            "parameters": {"type": "OBJECT", "properties": {"query": {"type": "STRING"}}, "required": ["query"]}
        },
        {
            "name": "data_analysis",
            "description": "Perform financial data analysis. Use this when comparing, analyzing trends, or finding insights from financial data.",
            "parameters": {"type": "OBJECT", "properties": {"query": {"type": "STRING"}}, "required": ["query"]}
        },
        {
            "name": "function_calling",
            "description": "Fetch real-time market data, stock prices, or perform financial calculations.",
            "parameters": {"type": "OBJECT", "properties": {"query": {"type": "STRING"}}, "required": ["query"]}
        },
        {
            "name": "direct_gemini_interaction",
            "description": "General conversation and knowledge-based queries.",
            "parameters": {"type": "OBJECT", "properties": {"query": {"type": "STRING"}}, "required": ["query"]}
        },
    ]
}

# Detect multiple tools needed
def suggest_tools(query):
    query = query.lower()
    
    tool_patterns = {
        "rag_query_resolver": [
            r"\b(who|what|when|where|explain|summary|definition|CEO|GDP|inflation)\b",
            r"\b(price|worth|stock|company|industry|market cap|headquarters)\b"
        ],
        "data_analysis": [
            r"\b(analyze|trend|compare|growth|forecast|historical|statistical|performance)\b",
            r"\b(over time|last year|past|years|quarters|revenue|profitability)\b"
        ],
        "function_calling": [
            r"\b(real-time|live|current|latest|today|now)\b",
            r"\b(fetch|get|retrieve)\b.*\b(news|price|quote|rate|exchange rate)\b",
            r"\b(calculate|convert|compute)\b"
        ],
        "direct_gemini_interaction": [
            r"\b(history|background|explain|overview|general|philosophy|internet)\b"
        ]
    }
    
    matched_tools = set()
    
    for tool, patterns in tool_patterns.items():
        for pattern in patterns:
            if re.search(pattern, query):
                matched_tools.add(tool)
    
    return list(matched_tools) if matched_tools else ["direct_gemini_interaction"]

def is_critical_mismatch(suggested, selected, query):
    """
    Determine if a mismatch between suggested and selected tools is critical.
    """
    critical_keywords = {
        "rag_query_resolver": r"\b(price|stock|market|rate|earnings|CEO|GDP)\b",
        "data_analysis": r"\b(analyze|trend|growth|compare|performance|forecast)\b",
        "function_calling": r"\b(real-time|current|latest|today|now|fetch|convert)\b"
    }
    
    for tool, pattern in critical_keywords.items():
        if tool in suggested and tool not in selected and re.search(pattern, query):
            return True
    
    return False

def log_mismatch(suggested_tools, selected_tools, query, outcome):
    """Log mismatches for later analysis"""
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "suggested_tools": suggested_tools,
            "selected_tools": selected_tools,
            "outcome": outcome
        }
        with open("./Data/tool_mismatch_log.jsonl", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"Failed to log mismatch: {e}")

def process_with_tools(tools, query_text):
    print(f"Processing with {tools}: {query_text}")
    return [{"tool": tool, "query": query_text, "status": "processed"} for tool in tools]

def function_call_gem(query: str) -> dict:
    """
    Calls Gemini AI with the provided query and retrieves function calls with improved precision.
    """
    client = genai.Client(api_key=genai_key)
    
    suggested_tools = suggest_tools(query)
    
    enhanced_query = f"""
    Query: {query}
    Based on the nature of this query, the most appropriate tools to use would likely be {suggested_tools}.
    """

    config = types.GenerateContentConfig(
        tools=[types.Tool(function_declarations=ALL_FUNCTIONS["tools"])]
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=enhanced_query,
            config=config
        )
        
        function_calls = getattr(response, "function_calls", [])
        
        selected_tools = list({fc.name for fc in function_calls} if function_calls else suggested_tools)
        
        critical_mismatch = is_critical_mismatch(suggested_tools, selected_tools, query)
        
        if critical_mismatch:
            log_mismatch(suggested_tools, selected_tools, query, "override")
            final_tools = suggested_tools
        else:
            log_mismatch(suggested_tools, selected_tools, query, "accepted")
            final_tools = selected_tools
        
        result = process_with_tools(final_tools, query)
        
        return {
            "status": "success",
            "original_query": query,
            "suggested_tools": suggested_tools,
            "selected_tools": selected_tools,
            "final_tools": final_tools,
            "function_calls": [{"name": fc.name, "args": getattr(fc, 'args', {})} for fc in function_calls],
            "result": result
        }
        
    except Exception as e:
        print(f"Error in function_call_gem: {e}")
        return {"status": "error", "tools": suggested_tools, "query": query, "error": str(e)}

# Example usage
def main():
    queries = [
        "What is the current price of Apple stock (AAPL)?",
        "Who is the CEO of JPMorgan Chase?",
        "Analyze the revenue growth of Microsoft over the past 5 years.",
        "Get the real-time stock quote for Google.",
        "What are some interesting facts about the history of finance?",
        "Analyze Tesla's stock trends and fetch its current price."
    ]
    
    for idx, query in enumerate(queries):
        print(f"\n=== Test Query {idx+1}: {query} ===")
        result = function_call_gem(query)
        print(f"Result: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    main()
