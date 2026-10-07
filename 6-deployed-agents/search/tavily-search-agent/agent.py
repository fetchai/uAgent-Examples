import os
from typing import List

import requests
from agent_health import tavily_account
from uagents import Context, Model
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.health import HealthProtocol, cached_check
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "<tavily-search-agent-seed>")
AGENT_NAME = os.getenv("AGENT_NAME", "Tavily Search Agent")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "<your-tavily-api-key>")
if TAVILY_API_KEY == "<your-tavily-api-key>":
    raise ValueError("Please provide your Tavily API key.")

PORT = 8000
agent = ChatAgent(
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
async def agent_is_healthy(ctx: Context) -> bool:
    return await cached_check(ctx, lambda: tavily_account(TAVILY_API_KEY))








health_protocol = HealthProtocol(
    agent_name=AGENT_NAME,
    check=agent_is_healthy,
)




agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
