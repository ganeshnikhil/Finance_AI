import google.generativeai as genai
from dotenv import load_dotenv
from os import environ



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

def data_prc_answer(query , data):
    
    try:
        model = configure_genai(genai_key)
        
        prmpt = f''' 
        Data: {data}  
        query : {query}
        '''
        
        # Step 3: Generate response
        response = model.generate_content(prmpt)
        # Step 4: Handle and return the response
        if response and hasattr(response, 'text'):
                return response.text.strip()
        else:
            return "Error: No response received from GenAI."
        
    except Exception as e:
        return f"Error: {str(e)}"
        