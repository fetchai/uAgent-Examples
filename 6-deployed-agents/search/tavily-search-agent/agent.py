import os
from enum import Enum
from typing import List

import requests
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "<tavily-search-agent-seed>")
AGENT_NAME = os.getenv("AGENT_NAME", "Tavily Search Agent")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "<your-tavily-api-key>")
if TAVILY_API_KEY == "<your-tavily-api-key>":
    raise ValueError("Please provide your Tavily API key.")

PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


class WebSearchRequest(Model):
    query: str


class WebSearchResult(Model):
    title: str
    url: str
    content: str


class WebSearchResponse(Model):
    query: str
    results: List[WebSearchResult]


proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Web-Search",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


def tavily_search(query) -> dict:
    """Perform a search using the Tavily Search API and return results."""
    endpoint = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "include_images": False,
        "include_answer": False,
        "include_raw_content": False,
        "max_results": 5,
        "include_domains": None,
        "exclude_domains": None,
    }

    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=10)
    except requests.exceptions.Timeout:
        return {"error": "The request timed out. Please try again."}
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}

    data = response.json()

    if "results" in data:
        return data["results"]

    return {"error": "No results found."}


@proto.on_message(WebSearchRequest, replies={WebSearchResponse, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: WebSearchRequest):
    try:
        search_results = tavily_search(msg.query)
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
        return

    if "error" in search_results:
        await ctx.send(sender, ErrorMessage(error=search_results["error"]))
        return

    await ctx.send(
        sender,
        WebSearchResponse(
            query=msg.query, results=[WebSearchResult(**r) for r in search_results]
        ),
    )


agent.include(proto, publish_manifest=True)


### Health check related code
def agent_is_healthy() -> bool:
    """
    Implement the actual health check logic here.

    For example, check if the agent can connect to a third party API,
    check if the agent has enough resources, etc.
    """
    condition = True  # TODO: logic here
    return bool(condition)


class HealthCheck(Model):
    pass


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class AgentHealth(Model):
    agent_name: str
    status: HealthStatus


health_protocol = QuotaProtocol(
    storage_reference=agent.storage, name="HealthProtocol", version="0.1.0"
)


@health_protocol.on_message(HealthCheck, replies={AgentHealth})
async def handle_health_check(ctx: Context, sender: str, msg: HealthCheck):
    status = HealthStatus.UNHEALTHY
    try:
        if agent_is_healthy():
            status = HealthStatus.HEALTHY
    except Exception as err:
        ctx.logger.error(err)
    finally:
        await ctx.send(sender, AgentHealth(agent_name=AGENT_NAME, status=status))


agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
