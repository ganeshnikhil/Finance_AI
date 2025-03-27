from src.Brain.sim_router import function_call_gem_gemini_similarity 
from src.Functions.exe_function import execute_routing_call




query = "what is finance?"
list_to_calls = function_call_gem_gemini_similarity(query)
for func in list_to_calls:
    solution = execute_routing_call(func)
    print(solution)

