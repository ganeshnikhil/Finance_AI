from google import genai
import re
from dotenv import load_dotenv
from os import environ

# Load environment variables from .env file
load_dotenv()

# Configure API key from environment variables
api_key = environ.get("genai_key")

# Initialize Gemini AI client
client = genai.Client(api_key=api_key)

# Define model name globally for consistency
model = "gemini-2.0-flash"


def direct_gemini_interaction(query: str) -> str:
    """
    Generates a detailed and structured financial response tailored to the Indian financial landscape.

    Args:
        query (str): The financial query for which insights are required.

    Returns:
        str: A structured and detailed response based on the query.
    """
    prompt = f"""
    You are a highly knowledgeable financial expert with deep expertise in the Indian financial landscape.
    Your expertise includes:
    - Indian stock market analysis, including NSE, BSE, Sensex, and Nifty indices.
    - Fundamental and technical analysis of Indian companies, sectoral performance, and regulatory updates.
    - Personal finance in India, such as budgeting, tax-saving schemes (ELSS, PPF, NPS), and retirement planning.
    - Investment options available in India, including mutual funds, SIPs, FD, PPF, NPS, bonds, and real estate.
    - Indian taxation laws (Income Tax, GST, Capital Gains), compliance, and strategies for minimizing tax liabilities.
    - Corporate finance concepts applicable to Indian businesses, such as capital structure, IPOs, and SEBI regulations.
    - Indian banking and fintech ecosystem, including UPI, digital payments, and RBI policies.
    - Cryptocurrency, blockchain trends, and RBI's stance on digital assets in India.
    
    Your task is to provide:
    - Accurate, data-driven, and well-reasoned responses that align with Indian financial regulations and trends.
    - Clear, concise explanations that offer actionable insights relevant to India.
    - Structured responses with key takeaways, considering the Indian economic context.
    - Caution about regulatory considerations, RBI guidelines, or market risks when necessary.
    
    Query: {query}
    Provide a detailed and structured response tailored specifically to the Indian financial environment.
    """
    try:
        # Generate response using Gemini AI
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        # Handle API errors and return appropriate message
        return f"Error while processing the query: {str(e)}"


def generate_financial_insights(data: list[str]) -> str:
    """
    Summarizes and extracts key financial insights from provided data.

    Args:
        data (list[str]): List of financial data or reports.

    Returns:
        str: Concise summary highlighting actionable insights, trends, and risks.
    """
    prompt = f"""
    You are a highly experienced financial analyst specializing in summarizing and extracting key insights from data related to:
    - Stock market news, trends, and sectoral updates.
    - Company financial statements, earnings reports, and balance sheet analysis.
    - Economic reports, RBI policies, and macroeconomic developments in India.
    - Investment and portfolio management strategies.
    - Corporate announcements, IPOs, mergers, and acquisitions.
    
    Your task is to:
    - Analyze the provided data and extract key insights or takeaways.
    - Focus on actionable insights, highlighting the broader implications without using excessive numerical values.
    - Provide a concise summary that emphasizes trends, risks, and opportunities.
    - Avoid detailed financial jargon or overly technical terms to ensure clarity.
    
    Provided Data:
    {data}

    Summarize the data and provide key insights in a structured and easy-to-understand format.
    """
    try:
        # Generate financial insights from the given data
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        # Handle API errors and return appropriate message
        return f"Error while generating insights: {str(e)}"


def get_ticker_symbol(query: str) -> list[str]:
    """
    Extracts stock ticker symbols from the given query.
    Adds '.NS' to the end of the ticker if the company is based in India.

    Args:
        query (str): The query containing company names.

    Returns:
        list[str]: List of extracted ticker symbols.
    """
    prompt = f"""
    Extract the stock ticker symbols from the following query.
    Return only the symbols without any extra text.
    If the company is based in India, add '.NS' to the end of the ticker symbol.
    Query: "{query}"
    
    Example:
    Input: "Show financials for Apple, Infosys, and Google."
    Output: ["AAPL", "INFY.NS", "GOOGL"]
    """
    try:
        # Generate response to extract ticker symbols
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )
        result = response.text

        # Extract ticker symbols using regex
        tickers = re.findall(r"[A-Z0-9]+(?:\.NS)?", result)

        return tickers
    except Exception as e:
        # Handle any errors and return an empty list with error message
        print(f"Error while extracting ticker symbols: {str(e)}")
        return []
