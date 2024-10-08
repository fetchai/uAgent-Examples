import os
import statistics

from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage

AGENT_SEED = os.getenv("AGENT_SEED")


class Prompt(Model):
    data: tuple[int | float, ...] | list[int | float] | set[int | float]


class Response(Model):
    mean: float
    median: float
    median_low: float
    median_high: float
    mode: float
    multi_mode: list[int | float]
    population_variance: float
    sample_variance: float
    population_standard_deviation: float
    sample_standard_deviation: float


PORT = 8000
agent = Agent(
    seed=AGENT_SEED,
    port=PORT,
    endpoint=f"http://localhost:{PORT}/submit",
)


proto = Protocol(name="Average-Statistics", version="0.1.0")


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(ctx.agent.address)


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


if __name__ == "__main__":
    agent.run()
