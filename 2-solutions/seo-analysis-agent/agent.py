import os
from enum import Enum

from seo_utils import compare_websites, extract_keywords, get_serp
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "your-seo-agent-seed>")
AGENT_NAME = os.getenv("AGENT_NAME", "SEO Analysis Agent")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEB_SCRAPER_AGENT_ADDRESS = os.getenv("website-scraper-agent")


class SEORequest(Model):
    url: str


class SEOResponse(Model):
    text: str


class WebsiteScraperRequest(Model):
    url: str


class WebsiteScraperResponse(Model):
    text: str


PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)

proto = QuotaProtocol(
    storage_reference=agent.storage, name="SEO-Analysis", version="0.1.0"
)


@proto.on_message(
    SEORequest,
    replies={WebsiteScraperRequest},
    rate_limit=RateLimit(window_size_minutes=60, max_requests=3),
)
async def handle_request(ctx: Context, sender: str, msg: SEORequest):
    agent_requests = agent.storage.get("agent_requests") or {}
    agent_requests[str(ctx.session)] = {
        "sender": sender,
        "url": msg.url,
    }
    await ctx.send(WEB_SCRAPER_AGENT_ADDRESS, WebsiteScraperRequest(url=msg.url))

    agent.storage.set("agent_requests", agent_requests)


@proto.on_message(
    WebsiteScraperResponse, replies={WebsiteScraperRequest, SEOResponse, ErrorMessage}
)
async def handle_web_response(ctx: Context, sender: str, msg: WebsiteScraperResponse):
    agent_requests = agent.storage.get("agent_requests") or {}
    session = str(ctx.session)
    if session not in agent_requests:
        return

    inferior_page_content = agent_requests[session].get("inferior_page_content")
    url = agent_requests[session]["url"]

    if not inferior_page_content:
        inferior_page_content = msg.text
        subject_keywords = extract_keywords(inferior_page_content, url)

        ctx.logger.info(f"Extracted keywords {subject_keywords}")

        top_pages = get_serp(subject_keywords)
        if not top_pages:
            await ctx.send(
                agent_requests[session]["sender"],
                SEOResponse(
                    text=(
                        "No search results found for the given keywords. "
                        "Please try again with different keywords."
                    )
                ),
            )
            agent_requests.pop(session)
            agent.storage.set("agent_requests", agent_requests)
            return

        agent_requests[session].update(
            {
                "inferior_page_content": inferior_page_content,
                "subject_keywords": subject_keywords,
                "top_url": top_pages[0],
            }
        )

        await ctx.send(
            WEB_SCRAPER_AGENT_ADDRESS, WebsiteScraperRequest(url=top_pages[0])
        )

        ctx.storage.set("agent_requests", agent_requests)
    else:
        top_url = agent_requests[session].get("top_url", "")
        subject_keywords = agent_requests[session].get("subject_keywords", "")
        superior_page_content = msg.text

        ctx.logger.info(f"Comparing {url} with {top_url}")

        result = compare_websites(
            superior_page_content, inferior_page_content, subject_keywords, top_url, url
        )

        await ctx.send(agent_requests[session]["sender"], SEOResponse(text=result))
        agent_requests.pop(session)
        agent.storage.set("agent_requests", agent_requests)


agent.include(proto)


# Health Check code
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
    await ctx.send(
        sender, AgentHealth(agent_name=AGENT_NAME, status=HealthStatus.HEALTHY)
    )


agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
