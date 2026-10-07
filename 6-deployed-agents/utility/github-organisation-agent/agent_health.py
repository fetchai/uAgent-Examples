"""Agent-local dependency health checks."""

import json
from urllib.request import Request, urlopen

PROBE_TIMEOUT_SECONDS = 5


def github_api() -> bool:
    url = "https://api.github.com/rate_limit"
    with urlopen(
        Request(url, headers={"User-Agent": "fetch-agent-health/1.0"}),
        timeout=PROBE_TIMEOUT_SECONDS,
    ) as response:
        payload = json.load(response)
    return "resources" in payload
