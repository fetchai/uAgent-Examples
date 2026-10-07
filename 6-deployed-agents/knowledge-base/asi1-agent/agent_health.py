"""Agent-local dependency health checks."""

import json
from urllib.request import Request, urlopen

PROBE_TIMEOUT_SECONDS = 5


def openai_chat(api_key: str | None, *, model: str, base_url: str) -> bool:
    """Run a one-token canary for compatible providers without a models endpoint."""
    url = f"{base_url.rstrip('/')}/chat/completions"
    data = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": "OK"}],
            "max_tokens": 1,
        }
    ).encode()
    with urlopen(
        Request(
            url,
            data=data,
            headers={
                "User-Agent": "fetch-agent-health/1.0",
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        ),
        timeout=PROBE_TIMEOUT_SECONDS,
    ) as response:
        payload = json.load(response)
    return bool(payload.get("choices"))
