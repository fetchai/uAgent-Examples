"""Agent-local dependency health checks."""

import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

PROBE_TIMEOUT_SECONDS = 5


def geoapify(api_key: str | None) -> bool:
    url = "https://api.geoapify.com/v2/places"
    params = {
        "categories": "parking",
        "filter": "circle:-0.1276,51.5072,1000",
        "limit": 1,
        "apiKey": api_key,
    }
    params = {key: value for key, value in params.items() if value is not None}
    url = f"{url}?{urlencode(params)}"
    with urlopen(
        Request(url, headers={"User-Agent": "fetch-agent-health/1.0"}),
        timeout=PROBE_TIMEOUT_SECONDS,
    ) as response:
        payload = json.load(response)
    return isinstance(payload.get("features"), list)
