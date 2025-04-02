import os
import requests
from typing import Dict
from uagents import Model, Field

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

if ALPHAVANTAGE_API_KEY is None:
    raise ValueError("You need to provide an API key for Alpha Vantage.")


class CompanyOverviewRequest(Model):
    ticker: str = Field(
        description="The stock ticker symbol (e.g., AAPL for Apple Inc.) used to identify the company on financial markets.", 
    )


class CompanyOverviewResponse(Model):
    overview: Dict[str, str]


def fetch_overview_json(ticker: str) -> dict:
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={ALPHAVANTAGE_API_KEY}"

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        return {"error": "The request timed out. Please try again."}
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}

    data = response.json()

    if not data or "Symbol" not in data:
        return {"error": "No valid data found in the response."}

    return data
