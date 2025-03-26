from uagents import Agent, Bureau, Context, Model

# Define response model
class RepairResponse(Model):
    status: str

# Define repair request model
class RepairRequest(Model):
    issue: str
    value: float



agent = Agent(name="repairer",
              seed="repairer seed phrase ouweufweif_838383",
              port=8002,
              endpoint=["http://localhost:8002/submit"])

# Repairer Agent (Handles repair requests)
@agent.on_message(model=RepairRequest)
async def handle_repair(ctx: Context, sender: str, msg: RepairRequest):
    ctx.logger.info(f"Received repair request from {sender}: {msg}")
    response = RepairResponse(status=f"Repair initiated for {msg.issue}")
    await ctx.send('agent1q0samncsypdkf5tp0kh7r2ep233vt79uerk50jlgxpnt3d5mhcw6ywjastg', response)
    ctx.logger.info(f"Sent repair response to 'agent1q0samncsypdkf5tp0kh7r2ep233vt79uerk50jlgxpnt3d5mhcw6ywjastg': {response}")
