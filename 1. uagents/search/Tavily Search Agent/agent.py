import os

import requests
from quota import RateLimiter
from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("Please provide your Tavily API key.")

PORT = 8000
agent = Agent(
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
    results: list[WebSearchResult]


proto = Protocol(name="Web-Search", version="0.1.0")

rate_limiter = RateLimiter(agent.storage)


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


@agent.on_event("startup")
async def introduce(ctx: Context):
    """This is only needed locally to check the agent's address."""
    ctx.logger.info(ctx.agent.address)


@proto.on_message(WebSearchRequest, replies={WebSearchResponse, ErrorMessage})
@rate_limiter.wrap
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

if __name__ == "__main__":
    agent.run()
