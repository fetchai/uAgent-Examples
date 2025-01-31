from uagents import Agent, Context

# Create an agent named Alice
alice = Agent(name="alice", seed="YOUR NEW PHRASE", port=8000, endpoint=["http://localhost:8000/submit"])

# Define a periodic task for Alice
@alice.on_interval(period=2.0)
async def say_hello(ctx: Context):
    ctx.logger.info(f'hello, my name is {alice.name}')


# Run the agent
if __name__ == "__main__":
    alice.run()