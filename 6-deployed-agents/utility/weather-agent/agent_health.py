"""Agent-local dependency health checks."""

import asyncio
import time
from collections.abc import Callable
from typing import Any

import requests

DEFAULT_TTL_SECONDS = 24 * 60 * 60
PROBE_TIMEOUT_SECONDS = 5


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


def weather_api(api_key: str | None) -> bool:
    response = requests.get(
        "https://api.weatherapi.com/v1/current.json",
        params={"key": api_key, "q": "London", "aqi": "no"},
        timeout=PROBE_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return "current" in response.json()
