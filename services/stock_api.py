import os
import requests
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

API_KEY = os.getenv("STOCKDATA_API_KEY")
BASE_URL = "https://api.stockdata.org/v1"


def get_quote(symbol):
    """Get current stock quote"""
    url = f"{BASE_URL}/data/quote"

    params = {
        "api_token": API_KEY,
        "symbols": symbol
    }

    response = requests.get(url, params=params)
    return response.json().get("data", [])


def get_eod(symbol):
    """Get historical EOD data"""
    url = f"{BASE_URL}/data/eod"

    params = {
        "api_token": API_KEY,
        "symbols": symbol,
        "interval": "day"
    }

    response = requests.get(url, params=params)
    return response.json().get("data", [])


def get_intraday(symbol):
    """Get intraday data"""
    url = f"{BASE_URL}/data/intraday"

    params = {
        "api_token": API_KEY,
        "symbols": symbol,
        "interval": "minute"
    }

    response = requests.get(url, params=params)
    return response.json().get("data", [])