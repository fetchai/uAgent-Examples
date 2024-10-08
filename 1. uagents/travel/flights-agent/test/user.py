from datetime import datetime

from uagents import Agent, Context, Field, Model


class FlightsSearchRequest(Model):
    origin: str = Field(
        description="This field is the airport IATA code for of the airport from where the user wants to fly from. This should be airport IATA code. IATA airport code is a three-character alphanumeric geocode.",
    )
    destination: str = Field(
        description="This field is the airport IATA code of the destination airport! This should be airport IATA code. IATA airport code is a three-character alphanumeric geocode."
    )
    date: datetime = Field(description="Contains the date of flying out.")
    persons: int = Field(description="Describes how many persons are going to fly.")
    currency: str = Field(
        default="USD",
        description="Currency, ISO 4217, in which you want to get information back (e.g.: EUR, GBP, USD, CHF...).",
    )


class Flight(Model):
    price: float
    price_formatted: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    airline: str


class FlightsSearchResponse(Model):
    flights: list[Flight]


agent = Agent()

flights_agent_address = (
    "agent1q24507dta3lgz5rwwk9gywgry29yajgz3zq6etx5q76jfeykax0gv7jfpjg"
)

msg_request = FlightsSearchRequest(
    origin="EDI",
    destination="BOS",
    date="2024-10-24T10:20",
    persons=2,
    currency="GBP",
)


@agent.on_event("startup")
async def agent_test_handler(ctx: Context):
    await ctx.send(flights_agent_address, msg_request)


@agent.on_message(model=FlightsSearchResponse)
async def show_results(ctx: Context, sender: str, msg: FlightsSearchResponse):
    ctx.logger.info(f"Heyy! We got response from '{sender[-10:]}'")
    ctx.logger.info(msg)


if __name__ == "__main__":
    agent.run()
