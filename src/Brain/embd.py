import google.generativeai as genai
from dotenv import load_dotenv
from os import environ 

load_dotenv()

api_key = genai.configure(environ.get("genai_key"))

def gen_embeddings(query):
        result = genai.embed_content(
                model="models/text-embedding-004",
                content=query)

        return result['embedding']