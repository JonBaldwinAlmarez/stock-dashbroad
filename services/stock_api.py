import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("STOCKDATA_API_KEY")

BASE_URL = "https://api.stockdata.org/v1/data/quote" # Base URL for the stock data API

def get_stock_quote(symbol: str):
    """Fetch the current stock price for a given symbol."""
    
    url = f"{BASE_URL}/qoute?symbols={symbol}&api_token={API_KEY}" # Construct the API URL with the symbol and API key

    try:
        response = requests.get(url) # Make the API request
        data = response.json() # Parse the JSON response

        if "data" in data and data["data"]:
            return data["data"][0] # Return the stock price if available
        else:
            return None

    except Exception as e:
        print(f"Error fetching qoute: {e}")


def get_historical_data(symbol: str, days: int = 30):
    """fetch historical stock data for a given symbol and number of days."""

    url = f"{BASE_URL}/ohlc?symbols={symbol}&api_token={API_KEY}&limit={days}" # Construct the API URL with the symbol, API key, and limit for the number of days

    try:
        response = requests.get(url) # Make the API request
        data = response.json() # Parse the JSON response

        if "data" in data and symbol in data["data"]:
            return data["data"][symbol]
        else:
            return None

    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return []


