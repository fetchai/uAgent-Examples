"""Agent-local dependency health checks."""

import json
from urllib.request import Request, urlopen

PROBE_TIMEOUT_SECONDS = 5


def open_charge_map(api_key: str | None) -> bool:
    url = "https://api.openchargemap.io/v3/referencedata"
    with urlopen(
        Request(
            url,
            headers={"User-Agent": "fetch-agent-health/1.0", "X-API-Key": str(api_key)},
        ),
        timeout=PROBE_TIMEOUT_SECONDS,
    ) as response:
        payload = json.load(response)
    return bool(payload)
