from uagents import Agent, Context, Model


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


agent = Agent()


AVERAGE_AGENT_ADDRESS = (
    "agent1q2e0n2r298mymaxmdux07vxyzxcu7u58c3xv94d6ky87xulxtechwncu9u2"
)

prompts = [
    (1, 6, 3, 7, 2, 5, 8, 3, 5, 12),  # tuple
    [-3, 5, 8, -2, 4, 6, 8, 3, 5, 12],  # list
    set([1.5, 6.3, 3.7, -7.2, 2.9, 5.8, 8.3, -5.5, 12.1]),  # set
]


@agent.on_event("startup")
async def handle_startup(ctx: Context):
    m = ctx.storage.get("matrix") or {}
    for prompt in prompts:
        ret = await ctx.send(AVERAGE_AGENT_ADDRESS, Prompt(data=prompt))
        ctx.logger.info(f"Sent prompt to AI agent: {prompt}")
        m[str(ret.session)] = {"prompt": list(prompt)}
    ctx.storage.set("matrix", m)


@agent.on_message(Response)
async def handle_response(ctx: Context, sender: str, msg: Response):
    m = ctx.storage.get("matrix") or {}
    ctx.logger.info(f"Received response from: {sender}")
    if str(ctx.session) not in m:  # this should never happen
        ctx.logger.error("Session not found in storage.")
        return
    m[str(ctx.session)]["response"] = msg.model_dump()
    ctx.storage.set("matrix", m)


if __name__ == "__main__":
    agent.run()
