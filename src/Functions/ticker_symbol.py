from google import genai
from dotenv import load_dotenv
from os import environ
import re

# Load environment variables
load_dotenv()
genai_key = environ.get("genai_key")

if "GOOGLE_API_KEY" not in environ:
    environ["GOOGLE_API_KEY"] = genai_key

# Initialize Gemini model
def initialize_gemini():
    return genai.GenerativeModel(model_name="gemini-1.5-flash")

# Function to get ticker symbols using Gemini
def get_ticker_symbols(query: str) -> list[str]:
    """
    Sends a query to Gemini and retrieves the list of mentioned ticker symbols.
    For Indian companies, appends `.NS` at the end of the symbol.
    
    Args:
    - query (str): User's input query to Gemini.
    
    Returns:
    - list[str]: List of detected ticker symbols with `.NS` appended for Indian companies.
    """
    # Initialize the Gemini model
    model = initialize_gemini()

    # Refined prompt to extract ticker symbols only
    refined_prompt = f"""
    Extract the stock ticker symbols from the following query.
    Return only the symbols without any extra text.
    If the company is based in India, add '.NS' to the end of the ticker symbol.
    Query: "{query}"
    
    Example:
    Input: "Show financials for Apple, Infosys, and Google."
    Output: ["AAPL", "INFY.NS", "GOOGL"]
    """

    # Generate response from Gemini
    response = model.generate_content(refined_prompt)

    # Extract the text and clean it
    result = response.text.strip()

    # Extract ticker symbols using regex
    tickers = re.findall(r"[A-Z0-9]+(?:\.NS)?", result)

    return tickers


# Example usage
if __name__ == "__main__":
    query = "Get the financials for Apple, Tata Motors, and Google."
    ticker_symbols = get_ticker_symbols(query)
    print(f"Detected Ticker Symbols: {ticker_symbols}")
