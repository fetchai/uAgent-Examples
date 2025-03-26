import random
from uagents import Agent, Bureau, Context, Model

# Define telemetry model
class Telemetry(Model):
    temperature: float
    vibration: float

# Define response model
class RepairResponse(Model):
    status: str

agent = Agent(name="machinery",
              seed="machinery seed phrase 09dkkefneff_93",
              port=8000,
              endpoint=["http://localhost:8000/submit"])


# Machinery Agent (Sends telemetry data)
@agent.on_interval(period=20.0)  # Sends telemetry every 20 seconds
async def send_telemetry(ctx: Context):
    telemetry = Telemetry(
        temperature=random.uniform(20, 100),
        vibration=random.uniform(0, 10)
    )
    await ctx.send('agent1qvk2ppctpjjj7ev6afdze3raup304pz7sc77sf6fk7h7n4uuexktx3t0der', telemetry)
    ctx.logger.info(f"Sent Telemetry: {telemetry}")

@agent.on_message(model=RepairResponse)
async def handle_repair(ctx: Context, sender: str, msg: RepairResponse):
    ctx.logger.info(f"Received repair info from {sender}: {msg.dict()}")
