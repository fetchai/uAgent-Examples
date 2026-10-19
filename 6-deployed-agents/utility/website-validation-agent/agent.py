import os
from typing import List

from crewai.tasks import TaskOutput
from grammar_check_agent_helper import (
    find_content_grammar_mistakes,
    scrape_website_text,
)
from uagents import Agent, Context, Model
from uagents.experimental.health import HealthProtocol
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








health_protocol = HealthProtocol(
    agent_name=AGENT_NAME,
    check=lambda _ctx: True,
)




agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
