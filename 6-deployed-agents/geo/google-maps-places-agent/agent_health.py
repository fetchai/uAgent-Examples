"""Agent-local dependency health checks."""

import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

PROBE_TIMEOUT_SECONDS = 5


def google_places(api_key: str | None) -> bool:
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": "parking in London", "key": str(api_key)}
    url = f"{url}?{urlencode(params)}"
    with urlopen(
        Request(url, headers={"User-Agent": "fetch-agent-health/1.0"}),
        timeout=PROBE_TIMEOUT_SECONDS,
    ) as response:
        payload = json.load(response)
    return payload.get("status") in {"OK", "ZERO_RESULTS"}
