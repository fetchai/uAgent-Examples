"""Agent-local dependency health checks."""

import json
from urllib.request import Request, urlopen

PROBE_TIMEOUT_SECONDS = 5


def _model_available(model_ids: set[str | None], model: str | None) -> bool:
    return model is None or any(
        (
            model_id == model or (model_id and model_id.startswith(f"{model}-"))
            for model_id in model_ids
        )
    )


def openai_models(
    api_key: str | None,
    *,
    model: str | None = None,
    base_url: str = "https://api.openai.com/v1",
) -> bool:
    url = f"{base_url.rstrip('/')}/models"
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
        payload = json.load(response)
    model_ids = {item.get("id") for item in payload.get("data", [])}
    return bool(model_ids) and _model_available(model_ids, model)
