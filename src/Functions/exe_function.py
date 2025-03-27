from src.Brain.query_res import rag_query_resolver 
from src.Brain.sql_agent import data_analysis 
from src.Brain.ask_gemini import direct_gemini_interaction 
from src.Brain.sim_router import function_call_gem_gemini_similarity
from src.Functions.finance_news import get_news_summary
from src.Functions.stock_analysis import get_stock_overview
from typing import Union
from Data.tools import TOOL_FUNCTIONS, TOOL_FUNCTION_EXAMPLES

# Mapping available routing functions
ROUTING_MAP = {
    "rag_query_resolver": rag_query_resolver,
    "data_analysis": data_analysis,
    "direct_gemini_interaction": direct_gemini_interaction,
    "function_calling": None,  # Placeholder for dynamic function execution
}

# Mapping available direct function calls
FUNCTION_MAP = {
    "get_news_summary": get_news_summary,
    "get_stock_overview": get_stock_overview,
}

def execute_routing_call(function_call: dict) -> Union[None, dict, list]:
    """
    Execute a function based on the function call dictionary.
    
    :param function_call: Dictionary with 'name' and 'parameters' keys.
    :return: Function output (dict/list) or None if execution fails.
    """
    output = None
    try:
        # Extract function name and parameters
        func_name = function_call.get("function")
        args = function_call.get("args")

        if not func_name:
            return None  # No function provided

        # Handling dynamic function calling
        if func_name == "Function_calling":
            list_of_tools = function_call_gem_gemini_similarity(args, ALL_FUNCTIONS=TOOL_FUNCTIONS, EXAMPLES=TOOL_FUNCTION_EXAMPLES)
            results = []

            for tool in list_of_tools:
                tool_name = tool.get("function")
                tool_params = tool.get("args")

                # Check if function exists in FUNCTION_MAP
                func = FUNCTION_MAP.get(tool_name)
                if not func:
                    print(f"[*] Function '{tool_name}' not found in FUNCTION_MAP.")
                    continue

                # Execute function with extracted parameters
                try:
                    all_parameters = [tool_params[k] for k in tool_params.keys()]
                    result = func(*all_parameters) if all_parameters else func()
                    results.append(result)
                except Exception as e:
                    print(f"[!] Error executing '{tool_name}': {e}")

            return results  # Return list of results from multiple tools

        # If it's a direct function from ROUTING_MAP
        func = ROUTING_MAP.get(func_name)

        if not func:
            print(f"[*] Function '{func_name}' not found in ROUTING_MAP.")
            return None

        # Execute function with parameters
        all_parameters = [args[k] for k in args.keys()]
        output = func(*all_parameters) if all_parameters else func()

    except KeyError as e:
        print(f"[!] Invalid function call format: Missing key {e}")
    except Exception as e:
        print(f"[!] Error executing function '{func_name}': {e}")

    return output  # Return final output
