"""Agent-local dependency health checks."""

import json
from urllib.request import Request, urlopen

PROBE_TIMEOUT_SECONDS = 5


def tavily_account(api_key: str | None) -> bool:
    url = "https://api.tavily.com/usage"
    with urlopen(
        Request(
            url,
            headers={
                "User-Agent": "fetch-agent-health/1.0",
                "Authorization": f"Bearer {api_key}",
            },
        ),
        timeout=PROBE_TIMEOUT_SECONDS,
    ) as response:
        json.load(response)
    return True
