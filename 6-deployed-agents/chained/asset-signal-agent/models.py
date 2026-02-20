from typing import List, Literal, Set

from uagents import Model


class AssetSignalRequest(Model):
    company_name: str


class AssetSignalResponse(Model):
    signal: Literal["BUY", "SELL", "WAIT"]
    price: float
    sources: Set[str]


# Ticker Resolver Agent
class TickerRequest(Model):
    company: str


class TickerResponse(Model):
    ticker: str


# Financial News Sentiment Agent
class FinancialNewsSentimentRequest(Model):
    ticker: str


class NewsSentiment(Model):
    title: str
    url: str
    summary: str
    overall_sentiment_label: str


class FinancialNewsSentimentResponse(Model):
    summary: List[NewsSentiment]


# Finbert Financial Sentiment Agent
class FinancialSentimentRequest(Model):
    text: str


class FinancialSentimentResponse(Model):
    positive: float
    neutral: float
    negative: float


# Stock Price Agent
class StockPriceRequest(Model):
    ticker: str


class StockPriceResponse(Model):
    text: str
