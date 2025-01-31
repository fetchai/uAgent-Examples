import os
from enum import Enum

import requests
from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "grammar-check-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Grammar Agent")
SAPLING_API_KEY = os.getenv("SAPLING_API_KEY")

if SAPLING_API_KEY is None:
    raise ValueError("You need to provide an API key for Sapling.")


class GrammarCheckRequest(Model):
    text: str


class GrammarCheckResponse(Model):
    corrected_text: str


PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


grammar_check_protocol = QuotaProtocol(
    storage_reference=agent.storage,
    name="Grammar Check Protocol",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


def check_grammar(text) -> dict:
    """
    Sends a request to the Sapling API to check the grammar of the provided text and returns the corrected text.

    Args:
        text (str): The input text to check.
    Returns:
        corrected_text (str): The corrected text.
    """
    try:
        response = requests.post(
            url="https://api.sapling.ai/api/v1/edits",
            headers={"Content-Type": "application/json"},
            json={
                "key": SAPLING_API_KEY,
                "text": text,
                "session_id": "test-session",
            },
            timeout=10,
        )

        if response.status_code == 200:
            results = response.json()
            edits = results.get("edits", [])
            return {"text": apply_corrections(text, edits)}

        return {"error": f"Error: {response.status_code} - {response.text}"}

    except requests.Timeout as e:
        return {"error": f"The request timed out: {str(e)}"}
    except requests.RequestException as e:
        return {"error": f"An error occurred during the request: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


def apply_corrections(text, edits) -> str:
    """
    Apply corrections to the original text based on the edit suggestions from
    Sapling API using the official Sapling edit logic.
    """
    # Ensure text is a string
    text = str(text)

    # Sort edits by the position they need to be applied at
    edits = sorted(
        edits, key=lambda e: (e["sentence_start"] + e["start"]), reverse=True
    )

    # Apply each edit to the text
    for edit in edits:
        start = edit["sentence_start"] + edit["start"]
        end = edit["sentence_start"] + edit["end"]

        # Check bounds to avoid errors
        if start > len(text) or end > len(text):
            continue

        # Apply the replacement
        text = text[:start] + edit["replacement"] + text[end:]

    return text


@grammar_check_protocol.on_message(
    model=GrammarCheckRequest, replies=GrammarCheckResponse
)
async def on_message(ctx: Context, sender: str, msg: GrammarCheckRequest):
    ctx.logger.info(f"Received text: {msg.text}")
    try:
        result = check_grammar(msg.text)

        if "error" in result:
            await ctx.send(sender, ErrorMessage(error=result["error"]))
            return

    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(sender, ErrorMessage(error=str(err)))
        return
    await ctx.send(sender, GrammarCheckResponse(corrected_text=result["text"]))


agent.include(grammar_check_protocol)


### Health check related code
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
