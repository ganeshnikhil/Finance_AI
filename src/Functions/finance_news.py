import yfinance as yf
from src.Brain.ask_gemini import generate_financial_insights


def get_company_news(ticker_symbol):
    """
    Fetches recent news articles related to a company using yfinance.

    Args:
        ticker_symbol (str): The stock ticker symbol of the company (e.g., 'AAPL' for Apple Inc.).

    Returns:
        list: A list of dictionaries containing news articles with title, publisher, publish time, and link.
    """
    try:
        # Get the Ticker object
        ticker = yf.Ticker(ticker_symbol)
        
        # Fetch news articles
        news = ticker.news if hasattr(ticker, "news") else []
        
        # Check if news is available
        if not news:
            print(f"No news available for {ticker_symbol}")
            return []

        return news

    except Exception as e:
        print(f"Error fetching news for {ticker_symbol}: {e}")
        return []


def yfinance_news(raw_news_data):
    """
    Format the raw news data retrieved from Yahoo Finance into a structured format.
    
    Args:
        raw_news_data (list): List of raw news articles from Yahoo Finance API.
        
    Returns:
        list: A list of formatted dictionaries containing news article details.
    """
    formatted_news = []
    
    for article in raw_news_data:
        # Safely extract article information
        formatted_article = {
            "title": article.get("title", "No Title"),
            "summary": article.get("summary", "No Summary Available"),
            "publisher": article.get("publisher", "Unknown Publisher"),
        }
        
        formatted_news.append(formatted_article)

    return formatted_news


def get_news_summary(ticker_symbol):
    """
    Fetches and formats recent news for a company and generates key insights.
    
    Args:
        ticker_symbol (str): The stock ticker symbol of the company.
        
    Returns:
        tuple: (Formatted News List, Key Insights from News)
    """
    # Get raw news data
    raw_news_data = get_company_news(ticker_symbol)

    # Format the news articles
    formatted_news = yfinance_news(raw_news_data)
    
    # Generate financial insights from the news
    key_insights = generate_financial_insights(formatted_news)
    return  key_insights
