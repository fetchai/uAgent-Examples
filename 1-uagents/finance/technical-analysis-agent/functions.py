import os

import requests
from uagents import Model

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

if ALPHAVANTAGE_API_KEY is None:
    raise ValueError("You need to provide an API key for Alpha Vantage.")


class IndicatorSignal(Model):
    indicator: str
    latest_value: float
    previous_value: float
    signal: str


# Function to fetch the indicator data
def get_indicator(symbol, interval, time_period, series_type, function):
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={ALPHAVANTAGE_API_KEY}"

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        raise
    except requests.exceptions.RequestException as e:
        raise ValueError("Request exception happened.") from e

    return response.json()


# Function to calculate the trading signal based on indicator values
def calculate_signal(latest_value, previous_value):
    if latest_value > previous_value:
        return "BUY"
    if latest_value < previous_value:
        return "SELL"
    return "HOLD"


# Function to analyze multiple indicators for a stock symbol
def analyze_stock(symbol) -> list[IndicatorSignal]:
    interval = "daily"
    time_period = 20
    series_type = "close"

    # List of all available indicators
    indicators = [
        "SMA",
        "EMA",
        "WMA",
        "DEMA",
        "TEMA",
        "TRIMA",
        "KAMA",
        "MAMA",
        "VWAP",
        "T3",
        "MACD",
        "RSI",
        "WILLR",
        "ADX",
        # "ADXR", "CCI", "CMO", "ROC", "ROCR", "AROON", "AROONOSC", "MFI", "TRIX",
        # "ULTOSC", "DX", "MINUS_DI", "PLUS_DI", "MINUS_DM", "PLUS_DM", "BBANDS",
        # "MIDPOINT", "MIDPRICE", "SAR", "TRANGE", "ATR", "NATR", "AD", "ADOSC", "OBV",
        # "HT_TRENDLINE", "HT_SINE", "HT_TRENDMODE", "HT_DCPERIOD", "HT_DCPHASE", "HT_PHASOR"
    ]

    results = []

    for indicator in indicators:
        try:
            data = get_indicator(symbol, interval, time_period, series_type, indicator)
            key = f"Technical Analysis: {indicator}"
            if key in data:
                latest_key = list(data[key].keys())[0]
                previous_key = list(data[key].keys())[1]
                latest_value = float(data[key][latest_key][indicator])
                previous_value = float(data[key][previous_key][indicator])
                signal = calculate_signal(latest_value, previous_value)
                results.append(
                    IndicatorSignal(
                        indicator=indicator,
                        latest_value=latest_value,
                        previous_value=previous_value,
                        signal=signal,
                    )
                )
        except Exception as e:
            print(f"Skipping indicator {indicator} due to error: {e}")

    return results
