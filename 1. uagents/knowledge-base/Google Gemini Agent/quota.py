"""
Provides a simple rate limiter for API requests.

The rate limiter uses an agent's storage to keep track of the number of requests
made by an agent within a given time window. If the number of requests exceeds
a specified limit, the rate limiter will block further requests until the time
window resets.

Usage:
- as a decorator for an agent handler function, using the `wrap` method
- by creating an inner function that you wrap with the rate limiter
- by calling the `add_request` method directly

Example:

```python
rate_limiter = RateLimiter(agent.storage)

@proto.on_message(<Prompt>, replies={<Response>, ErrorMessage})
@rate_limiter.wrap
async def handle_request(ctx: Context, sender: str, msg: Prompt):
    ...
```

```python
rate_limiter = RateLimiter(agent.storage)

@proto.on_message(<Prompt>, replies={<Response>, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: Prompt):
    # do some other processing here
    await inner_handle_request(ctx, sender, msg)


@rate_limiter.wrap
async def inner_handle_request(ctx: Context, sender: str, msg: Prompt):
    ...
```

```python
if rate_limiter.add_request(sender):
    await handle_request(ctx, sender, msg)
else:
    await ctx.send(sender, ErrorMessage(error="Rate limit exceeded. Try again later."))
```
"""

import os
from datetime import datetime
from typing import Any

from pydantic import BaseModel
from uagents import Context
from uagents.models import ErrorMessage
from uagents.storage import StorageAPI

WINDOW_SIZE_MINUTES = int(os.getenv("WINDOW_SIZE_MINUTES", "60"))
MAX_REQUESTS = int(os.getenv("MAX_REQUESTS", "6"))


class Usage(BaseModel):
    time_window_start: float
    requests: int


class RateLimiter:
    """
    Simple rate limiter for API requests.

    Uses agent storage with agent address as key to store the beginning of
    the most recent time window and the number of requests made in that window.
    """

    def __init__(
        self,
        storage: StorageAPI,
        window_size_minutes: int = WINDOW_SIZE_MINUTES,
        max_requests: int = MAX_REQUESTS,
    ):
        """
        Initialize the rate limiter.

        Args:
            storage: The storage API to use for storing the agent usage data
            window_size_minutes: The size of the time window in minutes
            max_requests: The maximum number of requests allowed in the time window
        """
        self.storage = storage
        self.window_size_minutes = window_size_minutes
        self.max_requests = max_requests

    def add_request(self, agent_address) -> bool:
        """
        Add a request to the rate limiter if the current time is still within the
        time window since the beginning of the most recent time window. Otherwise,
        reset the time window and add the request.

        Args:
            agent_address: The address of the agent making the request

        Returns:
            False if the maximum number of requests has been exceeded, True otherwise
        """

        now = datetime.now().timestamp()

        if self.storage.has(agent_address):
            usage = Usage(**self.storage.get(agent_address))

            if (now - usage.time_window_start) <= self.window_size_minutes * 60:
                if usage.requests >= self.max_requests:
                    return False
                usage.requests += 1
            else:
                usage.time_window_start = now
                usage.requests = 1
        else:
            usage = Usage(time_window_start=now, requests=1)

        self.storage.set(agent_address, usage.model_dump())

        return True

    def wrap(self, func):
        """
        Decorator to wrap a function with rate limiting.

        The order of wrapping is important. The rate limiter should be the innermost
        decorator to ensure that the rate limit is enforced before any other
        decorators are applied.

        Args:
            func: The function to wrap with rate limiting
        """

        async def decorator(ctx: Context, sender: str, msg: Any):
            if self.add_request(sender):
                await func(ctx, sender, msg)
            else:
                await ctx.send(
                    sender, ErrorMessage(error="Rate limit exceeded. Try again later.")
                )
            return

        return decorator
