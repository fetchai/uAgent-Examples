"""Agent-local dependency health checks."""

import json
from urllib.request import Request, urlopen

PROBE_TIMEOUT_SECONDS = 5


def huggingface_account(api_key: str | None) -> bool:
    url = "https://huggingface.co/api/whoami-v2"
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
