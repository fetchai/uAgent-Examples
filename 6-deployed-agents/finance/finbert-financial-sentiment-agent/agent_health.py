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



def _request_json(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if params:
        url = f"{url}?{urlencode({key: value for key, value in params.items() if value is not None})}"
    data = json.dumps(body).encode() if body is not None else None
    request_headers = {"User-Agent": "fetch-agent-health/1.0", **(headers or {})}
    if data is not None:
        request_headers.setdefault("Content-Type", "application/json")
    request = Request(
        url,
        data=data,
        headers=request_headers,
        method="POST" if data is not None else "GET",
    )
    try:
        with urlopen(request, timeout=PROBE_TIMEOUT_SECONDS) as response:
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
    """Run a bounded synchronous probe only when its stored result is stale."""
    now = int(time.time())
    cached = ctx.storage.get(cache_key)
    if isinstance(cached, dict):
        if now - cached.get("checked_at", 0) < ttl_seconds:
            healthy = bool(cached.get("healthy"))
            ctx.logger.info(
                f"Dependency health check [{cache_key}]: {('PASSED' if healthy else 'FAILED')} (cached result)"
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
        f"Dependency health check [{cache_key}]: {('PASSED' if healthy else 'FAILED')} (live probe)"
    )
    return healthy


def huggingface_account(api_key: str | None) -> bool:
    _request_json(
        "https://huggingface.co/api/whoami-v2",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    return True
