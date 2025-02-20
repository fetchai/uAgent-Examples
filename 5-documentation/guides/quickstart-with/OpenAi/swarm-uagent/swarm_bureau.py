from swarm import Swarm, Agent
from swarm import Agent as SwarmAgent
from uagents import Agent, Model, Bureau, Context

client = Swarm()


def transfer_to_agent_b():
    return swarm_agent_b


def transfer_to_agent_c():
    return swarm_agent_c


def helpful(context_variables):
    resp = "You are a quizzical agent. Answer their question in a riddle. Do not answer in a Haiku."
    ctx = context_variables["personality"] if context_variables["personality"] else ""
    print(ctx)
    if "friendly" in ctx:
        return f"{resp} be sure to give them lots of clues, make the riddle not too difficult to answer"
    else:
        return f"{resp}"


swarm_agent_a = SwarmAgent(
    name="Agent A",
    instructions="You are a helpful agent.",
    functions=[transfer_to_agent_b],
)

swarm_agent_b = SwarmAgent(
    name="Agent B",
    instructions="Only speak in Haikus. Find out what they want",
    functions=[transfer_to_agent_c]
)

swarm_agent_c = SwarmAgent(
    name="Agent C",
    instructions=helpful,
)

swarm_agent_d = SwarmAgent(
    name="Question generator",
    instructions="Create a random question to ask someone about any animal"
)


class Request(Model):
    text: str


class Response(Model):
    text: str


class QuestionCreation(Model):
    text: str


class QuestionCreated(Model):
    text: str


swarm_uagent = Agent(name='Swarm')
trigger_uagent = Agent(name='Trigger')
question_uagent = Agent(name='Question')


@swarm_uagent.on_message(Request)
async def handle_request(ctx: Context, sender: str, request: Request):
    response = client.run(
        agent=swarm_agent_a,
        messages=[{"role": "user", "content": request.text}],
    )

    await ctx.send(sender, Response(text=response.messages[-1]["content"]))


@trigger_uagent.on_event('startup')
async def trigger_request(ctx: Context):
    await ctx.send(swarm_uagent.address, Request(text="I want to talk to agent B."))


@trigger_uagent.on_message(Response)
async def handle_response(ctx: Context, sender: str, response: Response):
    print(f"Response from on_message : {response.text}")
    await ctx.send(question_uagent.address, QuestionCreation(text=""))


@trigger_uagent.on_message(QuestionCreated)
async def handle_response(ctx: Context, sender: str, response: Response):
    print(f"Response from on_message :", response.text)

    response = client.run(
        agent=swarm_agent_c,
        messages=[{"role": "user", "content": response.text}],
        context_variables={"user": "Jessica", "personality": "friendly, kind"}
    )

    print(response.messages[-1]["content"])


@question_uagent.on_message(QuestionCreation)
async def create_question(ctx: Context, sender: str, question: QuestionCreation):
    print("creating question...")

    response = client.run(
        agent=swarm_agent_d,
        messages=[{"role": "user", "content": "Create a random question about any animal"}],
    )

    print(response.messages[-1]["content"])

    await ctx.send(sender, QuestionCreated(text=response.messages[-1]["content"]))


bureau = Bureau()
bureau.add(swarm_uagent)
bureau.add(trigger_uagent)
bureau.add(question_uagent)
bureau.run()