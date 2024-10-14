"""
This agent is created to run on agentverse.ai
visit agentverse.ai to create an agent with this code.

This agent prints to console "hello my name is alice" every 5 seconds.
"""

agent.name = "alice"

@agent.on_interval(5)
async def interval_task(ctx: Context):
    """Implement interval task here"""
    ctx.logger.info(f'hello, my name is {agent.name}')