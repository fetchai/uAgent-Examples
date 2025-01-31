import random

from tinydb import Query, TinyDB
from uagents import Agent, Bureau, Context, Model

db = TinyDB("./db.json")

volume_supplier_agent = Agent(
    name="volume_supplier", seed="volume_supplier_seed_phrase"
)
volume_monitoring_agent = Agent(
    name="volume_monitor", seed="volume_monitor_seed_phrase"
)
diesel_consumer = Agent(name="diesel_comsumer", seed="diesel_seed_phrase")

TOTAL = 50000000


class RefillRequest(Model):
    fueltype: str
    current_volume: int


@volume_supplier_agent.on_message(model=RefillRequest)
async def handle_update_request(ctx: Context, sender: str, msg: RefillRequest):
    Fuel = Query()
    table = db.table("fuel")
    result = table.search(Fuel.fueltype == "diesel")

    ctx.logger.info("increasing volume by 200")

    if result:
        ctx.logger.info(f"current volume = {result[0]['volume']}")
        new_volume = result[0]["volume"] + 200
        table.update({"volume": new_volume}, Fuel.fueltype == "diesel")


@volume_monitoring_agent.on_interval(period=10.0)
async def fetch_all_employee_details(ctx: Context):
    Fuel = Query()
    table = db.table("fuel")
    result = table.search(Fuel.fueltype == "diesel")

    if result:
        if TOTAL > result[0]["volume"]:
            await ctx.send(
                volume_supplier_agent.address,
                RefillRequest(fueltype="diesel", current_volume=result[0]["volume"]),
            )


@diesel_consumer.on_interval(period=5.0)
async def consuming_diesel(ctx: Context):
    Fuel = Query()
    table = db.table("fuel")
    result = table.search(Fuel.fueltype == "diesel")

    if result:
        consumed = random.randint(1, 100)
        new_volume = max(0, result[0]["volume"] - consumed)
        ctx.logger.info(f"Consuming_diesel {consumed}")
        table.update({"volume": new_volume}, Fuel.fueltype == "diesel")
    else:
        ctx.logger.info("no match consuming_diesel")


bureau = Bureau()
bureau.add(volume_supplier_agent)
bureau.add(volume_monitoring_agent)
bureau.add(diesel_consumer)

if __name__ == "__main__":
    bureau.run()
