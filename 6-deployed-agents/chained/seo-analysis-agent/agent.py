import os
from enum import Enum

from seo_utils import compare_websites, extract_keywords, get_serp
from uagents import Agent, Context, Model
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

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
agent = ChatAgent(
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
    replies={SEOResponse, ErrorMessage},
    rate_limit=RateLimit(window_size_minutes=60, max_requests=3),
)
async def handle_request(ctx: Context, sender: str, msg: SEORequest):
    if not WEB_SCRAPER_AGENT_ADDRESS:
        ctx.logger.info("WEB_SCRAPER_AGENT_ADDRESS is not set")
        return

    inferior_reply, inferior_status = await ctx.send_and_receive(
        WEB_SCRAPER_AGENT_ADDRESS,
        WebsiteScraperRequest(url=msg.url),
        response_type=WebsiteScraperResponse,
    )
    if not isinstance(inferior_reply, WebsiteScraperResponse):
        await ctx.send(sender, ErrorMessage(error=f"Scraper failed for target URL: {inferior_status}"))
        return

    inferior_page_content = inferior_reply.text or ""
    if not inferior_page_content.strip():
        await ctx.send(sender, ErrorMessage(error="Scraper returned empty content for the target URL"))
        return

    subject_keywords = extract_keywords(inferior_page_content, msg.url)
    top_pages = get_serp(subject_keywords)
    if not top_pages:
        await ctx.send(
            sender,
            SEOResponse(
                text=(
                    "No search results found for the given keywords. "
                    "Please try again with different keywords."
                )
            ),
        )
        return

    top_url = top_pages[0]

    superior_reply, superior_status = await ctx.send_and_receive(
        WEB_SCRAPER_AGENT_ADDRESS,
        WebsiteScraperRequest(url=top_url),
        response_type=WebsiteScraperResponse,
    )
    if not isinstance(superior_reply, WebsiteScraperResponse):
        await ctx.send(sender, ErrorMessage(error=f"Scraper failed for competitor URL: {superior_status}"))
        return

    superior_page_content = superior_reply.text or ""
    if not superior_page_content.strip():
        await ctx.send(sender, ErrorMessage(error="Scraper returned empty content for the competitor URL"))
        return

    result = compare_websites(
        superior_page_content,
        inferior_page_content,
        subject_keywords,
        top_url,
        msg.url,
    )
    await ctx.send(sender, SEOResponse(text=result))


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
