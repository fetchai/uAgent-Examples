import random
from uagents import Agent, Bureau, Context, Model

# Define telemetry model
class Telemetry(Model):
    temperature: float
    vibration: float

# Define repair request model
class RepairRequest(Model):
    issue: str
    value: float

agent = Agent(name="monitor",
              seed="monitor seed phrase piwefgp99_iwefpie",
              port=8001,
              endpoint=["http://localhost:8001/submit"])

# Monitor Agent (Applies threshold rules to check anomalies)
@agent.on_message(model=Telemetry)
async def analyze_telemetry(ctx: Context, sender: str, msg: Telemetry):
    ctx.logger.info(f"Received telemetry from {sender}: {msg}")
    if msg.temperature > 80:
        request = RepairRequest(issue="High Temperature", value=msg.temperature)
        await ctx.send('agent1qt5k53m7p3qt6kshx46g8jgg4drr8dczrgvkt5xuyl303scclmxuv4556sw', request)
        await ctx.send(sender, request)  # Notify sender
        ctx.logger.info(f"High Temp! Sent repair request: {request} to 'agent1qt5k53m7p3qt6kshx46g8jgg4drr8dczrgvkt5xuyl303scclmxuv4556sw' and {sender}")
    elif msg.vibration > 7:
        request = RepairRequest(issue="High Vibration", value=msg.vibration)
        await ctx.send('agent1qt5k53m7p3qt6kshx46g8jgg4drr8dczrgvkt5xuyl303scclmxuv4556sw', request)
        await ctx.send(sender, request)  # Notify sender
        ctx.logger.info(f"High Vibration! Sent repair request: {request} to 'agent1qt5k53m7p3qt6kshx46g8jgg4drr8dczrgvkt5xuyl303scclmxuv4556sw' and {sender}")
    else:
        ctx.logger.info("Telemetry Normal")
