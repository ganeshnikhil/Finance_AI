import google.generativeai as genai
from dotenv import load_dotenv
from os import environ
from src.Data.prompts import question, structured_prompt
import json 
import re 

# Load environment variables
load_dotenv()
genai_key = environ.get("genai_key")


def configure_genai(api_key):
    """
    Configures the GenAI API with the given API key.
    """
    if not api_key:
        raise ValueError("API key for GenAI is not provided.")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def construct_prompt(user_query):
    """
    Constructs the structured prompt for generating SQL queries.
    
    """
    question["user_question"] = user_query
    return f"{structured_prompt}\n{question}"

def parse_json(text):
    json_match = re.search(r"```json\n(.*?)\n```", text, re.DOTALL)
    if json_match:
        json_string = json_match.group(1)  # Extract JSON content
        data = json.loads(json_string)  # Parse JSON
        return data 
    print("No valid JSON found!")
    return None 

    

def generate_sql_query(user_query):
    """
    Generates an SQL query based on the user's question using Google GenAI.
    """
    try:
        # Step 1: Configure GenAI
        model = configure_genai(genai_key)
        
        # Step 2: Construct the prompt
        prompt = construct_prompt(user_query)
        
        # Step 3: Generate response
        response = model.generate_content(prompt)
        print(response.parts[0].text)
        # Step 4: Handle and return the response
        if response and hasattr(response, 'text'):
            # Parse the response text as JSON
            result = json.loads(response.text.strip())
            return result 
    except Exception as e:
        print(f"Error:{e}")
        
    #         # Validate the output format
    #         if "sql_query" in result:
    #             return result
    #         else:
    #             return {
    #                 "sql_query": "",
    #                 "clarification_note": "The response did not include a valid SQL query."
    #             }
    #     else:
    #         return {
    #             "sql_query": "",
    #             "clarification_note": "No response received from GenAI."
    #         }
    # except Exception as e:
    #     return {
    #         "sql_query": "",
    #         "clarification_note": f"Error: {str(e)}"
    #     }