
from google import genai
from google.genai import types
from dotenv import load_dotenv
from os import environ
import numpy as np
from Data.tools import ROUTING_MAP_FUNCTIONS , ROUTING_MAP_EXAMPLES
from numpy.linalg import norm
import re 
import json 

# Load environment variables
load_dotenv()
genai_key = environ.get("genai_key")

EMBEDDING_MODEL = "models/embedding-001"

def get_gemini_embeddings(texts):
    """Generates embeddings using Gemini API in batches."""
    client = genai.Client(api_key=genai_key)
    try:
        response = client.models.embed_content(model=EMBEDDING_MODEL, contents=texts)
        return [np.array(embd.values) for embd in response.embeddings]
    except Exception as e:
        print(f"Error getting Gemini embeddings: {e}")
        return [None] * len(texts)

def cosine_similarity(a, b):
    if a is None or b is None:
        return 0.0
    return np.dot(a, b) / (norm(a) * norm(b))

def get_similar_examples_gemini(query, examples, top_n=10):
    """Retrieves the top N most similar examples using Gemini embeddings."""
    query_embedding = get_gemini_embeddings([query])[0] # embedding of the query.

    example_texts = [e['query'] for e in examples]
    example_embeddings = get_gemini_embeddings(example_texts) # batch embedding of examples.
    similarity_scores = [cosine_similarity(query_embedding, emb) for emb in example_embeddings]
    top_results = sorted(range(len(similarity_scores)), key=lambda i: similarity_scores[i], reverse=True)[:top_n]

    return [examples[i] for i in top_results]


def parse_json_markdown(json_string: str) -> dict:
    # Try to find JSON string within first and last triple backticks
    match = re.search(r"""```       # match first occuring triple backticks
                          (?:json)? # zero or one match of string json in non-capturing group
                          (.*)```   # greedy match to last triple backticks""", json_string, flags=re.DOTALL|re.VERBOSE)

    # If no match found, assume the entire string is a JSON string
    if match is None:
        json_str = json_string
    else:
        # If match found, use the content within the backticks
        json_str = match.group(1)

    # Strip whitespace and newlines from the start and end
    json_str = json_str.strip()

    # Parse the JSON string into a Python dictionary while allowing control characters by setting strict to False
    parsed = json.loads(json_str, strict=False)

    return parsed

def function_call_gem_gemini_similarity(query:str , ALL_FUNCTIONS:dict = ROUTING_MAP_FUNCTIONS , EXAMPLES:dict = ROUTING_MAP_EXAMPLES):
    client = genai.Client(api_key=genai_key)
    config = types.GenerateContentConfig(
        tools=[types.Tool(function_declarations=ALL_FUNCTIONS["tools"])],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
    )
    
    # Get similar examples for context
    similar_examples = get_similar_examples_gemini(query, EXAMPLES)
    example_string = "\n".join([
        f"Query: {e['query']}\nFunction: {e['function_call']}\nArgs: {e['args']}" 
        for e in similar_examples
    ])

    user_prompt = f"""
    Here are the most similar example queries and their expected function calls:
    {example_string}

    Your Query: {query}
    Predict the most appropriate function and required parameters in list of  json objects , without executing it.
    """
    
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[{"role": "user", "parts": [{"text": user_prompt}]}],
            config=config
        ) 
        
        result = parse_json_markdown(response.text)

        return result
        
    except Exception as e:
        print(f"Error: {e}")
        return []
