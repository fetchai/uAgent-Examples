import os
from enum import Enum

import requests
from bs4 import BeautifulSoup
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "website-scraper-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Website Scraper Agent")


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
    storage_reference=agent.storage, name="Website-Scraping-Protocol", version="0.1.0"
)


async def get_webpage_content(url) -> str:
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            response_text = response.text
            soup = BeautifulSoup(response_text, "html.parser")

            # Remove unwanted tags
            for script_or_style in soup(
                ["script", "style", "header", "footer", "nav", "aside"]
            ):
                script_or_style.decompose()

            # Extract text from paragraph tags
            text_blocks = soup.find_all("p")
            text_content = " ".join(
                block.get_text(strip=True)
                for block in text_blocks
                if block.get_text(strip=True)
            )

            # Limit to first 500 words for summary
            words = text_content.split()
            limited_text = " ".join(words)
            return limited_text
        return (
            f"Error: Unable to fetch content due to HTTP Status {response.status_code}"
        )

    except Exception as e:
        return "Error encountered: " + str(e)


@proto.on_message(WebsiteScraperRequest, replies={WebsiteScraperResponse, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: WebsiteScraperRequest):
    ctx.logger.info(f"Received request for URL: {msg.url}")
    try:
        content = await get_webpage_content(msg.url)
        await ctx.send(sender, WebsiteScraperResponse(text=content))
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(sender, ErrorMessage(error=str(err)))


agent.include(proto, publish_manifest=True)


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
