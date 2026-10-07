"""Agent-local dependency health checks."""


import requests

PROBE_TIMEOUT_SECONDS = 5


def weather_api(api_key: str | None) -> bool:
    response = requests.get(
        "https://api.weatherapi.com/v1/current.json",
        params={"key": api_key, "q": "London", "aqi": "no"},
        timeout=PROBE_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return "current" in response.json()
