import os
from enum import Enum
from typing import List

from crewai.tasks import TaskOutput
from grammar_check_agent_helper import (
    find_content_grammar_mistakes,
    scrape_website_text,
)
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage
from website_utils import find_broken_links

AGENT_NAME = os.getenv("AGENT_NAME", "Website Validation Agent")
AGENT_SEED = os.getenv("AGENT_SEED")

PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


class WebsiteValidationInput(Model):
    website_url: str


class GrammarMistake(Model):
    error: str
    solution: str


class WebsiteValidationResponse(Model):
    invalid_links: List[str]
    grammar_mistakes: List[GrammarMistake]


proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Website-Validation",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


@proto.on_message(
    model=WebsiteValidationInput, replies={WebsiteValidationResponse, ErrorMessage}
)
async def message_handler(ctx: Context, sender: str, msg: WebsiteValidationInput):
    ctx.logger.info(f"Received website validation request for url: {msg.website_url}.")
    formatted_mistakes = []
    try:
        invalid_links = find_broken_links(url=msg.website_url)
        scrapped_content = scrape_website_text(url=msg.website_url)
        grammar_mistakes: TaskOutput = find_content_grammar_mistakes(
            content=scrapped_content
        )

        if "errors" in grammar_mistakes.json_dict:
            for error in grammar_mistakes.json_dict["errors"]:
                formatted_mistakes.append(
                    GrammarMistake(error=error["error"], solution=error["solution"])
                )

    except Exception as e:
        ctx.logger.error(f"Something went wrong while validating: {e}")
        await ctx.send(
            sender, ErrorMessage(error="Something went wrong while validating.")
        )
        return

    if not invalid_links and not formatted_mistakes:
        await ctx.send(
            sender,
            ErrorMessage(error="No result found for the given website URL."),
        )
        return

    await ctx.send(
        sender,
        WebsiteValidationResponse(
            invalid_links=invalid_links,
            grammar_mistakes=formatted_mistakes,
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
