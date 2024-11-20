from uagents import Agent, Context

agent = Agent(name="Hosted", seed="your_seed_phrase", port=8000, endpoint=["http://127.0.0.1:8000/submit"])

global_counter = 0

@agent.on_interval(period=1.0)
async def on_interval(ctx: Context):
    global global_counter

    # increment the global counter - bad!
    global_counter += 1

    current_count = int(ctx.storage.get("count") or 0)
    current_count += 1

    ctx.logger.info(f"My count is: {current_count}")
    ctx.logger.info(f"My global is: {global_counter}")

    ctx.storage.set("count", current_count)

if __name__ == "__main__":
    agent.run()