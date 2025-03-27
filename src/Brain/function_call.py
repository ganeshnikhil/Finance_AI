from src.Brain.sim_router import function_call_gem_gemini_similarity 
from Data.tools import TOOL_FUNCTIONS , TOOL_FUNCTION_EXAMPLES


def function_calling(query:str):
    func_calls = function_call_gem_gemini_similarity(query , ALL_FUNCTIONS=TOOL_FUNCTIONS ,EXAMPLES=TOOL_FUNCTION_EXAMPLES)
    
