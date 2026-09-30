"""Agent-local dependency health checks."""

import asyncio
import json
import time
from collections.abc import Callable
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

DEFAULT_TTL_SECONDS = 24 * 60 * 60
PROBE_TIMEOUT_SECONDS = 5



def _request_json(
    url: str,
    *,
    headers: dict[str, str],
    body: dict[str, Any],
) -> dict[str, Any]:
    request = Request(
        url,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
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


def sapling_account(api_key: str | None) -> bool:
    _request_json(
        "https://api.sapling.ai/api/v1/reporting/api_quota_usage",
        headers={"Authorization": f"Bearer {api_key}"},
        body={},
    )
    return True
