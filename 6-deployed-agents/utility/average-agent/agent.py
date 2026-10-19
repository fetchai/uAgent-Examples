import os
import statistics

from average import get_statistics
from messages import Prompt, Response
from uagents import Context
from uagents.experimental.chat_agent import ChatAgent
from uagents.experimental.health import HealthProtocol
from uagents.experimental.quota import QuotaProtocol
from uagents_core.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "average-test-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Average Agent")


PORT = 8000
agent = ChatAgent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


proto = QuotaProtocol(
    storage_reference=agent.storage, name="Average-Statistics", version="0.1.0"
)


@proto.on_message(Prompt, replies={Response, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: Prompt):
    try:
        math = get_statistics(msg)
    except statistics.StatisticsError as s_err:
        await ctx.send(sender, ErrorMessage(error=str(s_err)))
        return
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
        return
    await ctx.send(sender, math)


agent.include(proto, publish_manifest=True)


# Health Check code






health_protocol = HealthProtocol(
    agent_name=AGENT_NAME,
    check=lambda _ctx: True,
)




agent.include(health_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
