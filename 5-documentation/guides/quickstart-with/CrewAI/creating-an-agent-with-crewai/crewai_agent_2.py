from uagents import Agent, Context, Model


class CityRequestModel(Model):
    city: str


class ResearchReportModel(Model):
    report: str


research_asking_agent = Agent(
    name="research_asking_agent",
    seed="research_asking_agent_seed",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

TARGET_AGENT_ADDRESS = (
    "agent1qgxfhzy78m2qfdsg726gtj4vnd0hkqx96xwprng2e4rmn0xfq7p35u6dz8q"
)
DEFAULT_CITY = "London"


@research_asking_agent.on_event("startup")
async def on_startup(ctx: Context):
    """
    Triggered when the agent starts up.

    What it does:
    - Logs the agent's name and address.
    - Sends a message to the target agent with the default city (e.g., 'London').

    Parameters:
    - ctx: Context, provides the execution context for logging and messaging.

    Returns:
    - None: Sends the message to the target agent asynchronously.
    """
    ctx.logger.info(
        f"Hello, I'm {research_asking_agent.name}, and my address is {research_asking_agent.address}."
    )

    await ctx.send(TARGET_AGENT_ADDRESS, CityRequestModel(city=DEFAULT_CITY))


@research_asking_agent.on_message(model=ResearchReportModel)
async def handle_research_report(ctx: Context, sender: str, msg: ResearchReportModel):
    """
    Triggered when a message of type ResearchReportModel is received.

    What it does:
    - Logs the sender's address and the research report received.

    Parameters:
    - ctx: Context, provides the execution context for logging and messaging.
    - sender: str, the address of the sender agent.
    - msg: ResearchReportModel, the received research report.

    Returns:
    - None: Processes the message and logs it.
    """
    ctx.logger.info(f"Received research report from {sender}: {msg.report}")


if __name__ == "__main__":
    """
    Starts the research analyst agent and begins listening for events.

    What it does:
    - Runs the agent, enabling it to send/receive messages and handle events.

    Returns:
    - None: Runs the agent loop indefinitely.
    """
    research_asking_agent.run()