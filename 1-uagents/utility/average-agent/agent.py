import os
import statistics
from enum import Enum
from typing import List, Set, Tuple, Union

from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED", "average-test-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Average Agent")


class Prompt(Model):
    data: Union[
        Tuple[Union[int, float]], List[Union[int, float]], Set[Union[int, float]]
    ]


class Response(Model):
    mean: float
    median: float
    median_low: float
    median_high: float
    mode: float
    multi_mode: List[Union[int, float]]
    population_variance: float
    sample_variance: float
    population_standard_deviation: float
    sample_standard_deviation: float


PORT = 8000
agent = Agent(
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
        math = Response(
            mean=statistics.mean(msg.data),
            median=statistics.median(msg.data),
            median_low=statistics.median_low(msg.data),
            median_high=statistics.median_high(msg.data),
            mode=statistics.mode(msg.data),
            multi_mode=statistics.multimode(msg.data),
            population_variance=statistics.pvariance(msg.data),
            sample_variance=statistics.variance(msg.data),
            population_standard_deviation=statistics.pstdev(msg.data),
            sample_standard_deviation=statistics.stdev(msg.data),
        )
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
