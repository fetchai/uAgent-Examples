"""Agent-local dependency health checks."""

import asyncio
import json
import time
from collections.abc import Callable
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEFAULT_TTL_SECONDS = 24 * 60 * 60
PROBE_TIMEOUT_SECONDS = 5



def _request_json(url: str, *, params: dict[str, Any]) -> dict[str, Any]:
    url = f"{url}?{urlencode(params)}"
    try:
        with urlopen(
            Request(url, headers={"User-Agent": "fetch-agent-health/1.0"}),
            timeout=PROBE_TIMEOUT_SECONDS,
        ) as response:
            return json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"provider returned HTTP {error.code}") from error


async def cached_check(
    ctx: Any,
    probe: Callable[[], bool],
    *,
    cache_key: str = "dependency_health",
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
) -> bool:
    now = int(time.time())
    cached = ctx.storage.get(cache_key)
    if isinstance(cached, dict):
        if now - cached.get("checked_at", 0) < ttl_seconds:
            healthy = bool(cached.get("healthy"))
            ctx.logger.info(
                f"Dependency health check [{cache_key}]: "
                f"{'PASSED' if healthy else 'FAILED'} (cached result)"
            )
            return healthy
    try:
        healthy = bool(
            await asyncio.wait_for(
                asyncio.to_thread(probe), timeout=PROBE_TIMEOUT_SECONDS + 1
            )
        )
    except Exception as error:
        ctx.logger.warning(f"Dependency health check failed: {error}")
        healthy = False
    ctx.storage.set(cache_key, {"checked_at": now, "healthy": healthy})
    ctx.logger.info(
        f"Dependency health check [{cache_key}]: "
        f"{'PASSED' if healthy else 'FAILED'} (live probe)"
    )
    return healthy


def google_places(api_key: str | None) -> bool:
    payload = _request_json(
        "https://maps.googleapis.com/maps/api/place/textsearch/json",
        params={"query": "parking in London", "key": str(api_key)},
    )
    return payload.get("status") in {"OK", "ZERO_RESULTS"}
