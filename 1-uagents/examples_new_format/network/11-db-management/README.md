# Room Booking Example

![domain:uAgents101](https://img.shields.io/badge/uAgents--101-3D8BD3?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMCAwLjVDMCAwLjIzNDM3NSAwLjIxODc1IDAgMC41IDBIMS41QzEuNzY1NjIgMCAyIDAuMjM0Mzc1IDIgMC41VjEuNUgwVjAuNVpNMCAySDJWNkgwVjJaTTAgNi41SDJWNy41QzIgNy43ODEyNSAxLjc2NTYyIDggMS41IDhIMC41QzAuMjE4NzUgOCAwIDcuNzgxMjUgMCA3LjVWNi41Wk0yLjUgMC41QzIuNSAwLjIzNDM3NSAyLjcxODc1IDAgMyAwSDRDNC4yNjU2MiAwIDQuNSAwLjIzNDM3NSA0LjUgMC41VjEuNUgyLjVWMC41Wk0yLjUgMkg0LjVWNkgyLjVWMlpNMi41IDYuNUg0LjVWNy41QzQuNSA3Ljc4MTI1IDQuMjY1NjIgOCA0IDhIM0MyLjcxODc1IDggMi41IDcuNzgxMjUgMi41IDcuNVY2LjVaTTUuNjcxODggNi4yMDMxMkw1IDMuNjQwNjJWMi4yMzQzOEw2LjU2MjUgMS44MTI1TDcuNTkzNzUgNS42ODc1TDUuNjcxODggNi4yMDMxMlpNNi40Mzc1IDEuMzI4MTJMNSAxLjcxODc1VjAuMTcxODc1TDUuNTYyNSAwLjAzMTI1QzUuODI4MTIgLTAuMDQ2ODc1IDYuMTA5MzggMC4xMDkzNzUgNi4xNzE4OCAwLjM3NUw2LjQzNzUgMS4zMjgxMlpNNS43OTY4OCA2LjY3MTg4TDcuNzE4NzUgNi4xNzE4OEw3Ljk2ODc1IDcuMTI1QzguMDQ2ODggNy4zOTA2MiA3Ljg5MDYyIDcuNjU2MjUgNy42MjUgNy43MzQzOEw2LjY3MTg4IDcuOTg0MzhDNi40MDYyNSA4LjA2MjUgNi4xMjUgNy45MDYyNSA2LjA2MjUgNy42NDA2Mkw1Ljc5Njg4IDYuNjcxODhaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)

Welcome to the Room Booking example! This guide demonstrates how to create a distributed agent system where a guest can request a room booking from a hotel. This example focuses on using Tortoise ORM for database management within the agents to handle room availability and booking processes. 

To prepare for running the example, ensure you're in the proper directory and have configured your environment with the necessary dependencies:

```
poetry install
poetry shell
```
## Using Tortoise ORM for Database Management

### Defining the Models

- **Description**: Models are used to define the structure of the data exchanged between agents. In this example, we have `RoomRequest` and `RoomResponse` models for the booking request and response, and an `Availability` model for managing room availability and pricing.

```python
from uagents import Model
from tortoise import fields, models

class RoomRequest(Model):
    max_price: int

class RoomResponse(Model):
    success: bool

class Availability(models.Model):
    id = fields.IntField(pk=True)
    room_available = fields.BooleanField(default=True)
    min_price = fields.FloatField(default=0.0)
```

### Hotel Agent with Tortoise ORM

- **Description**: The hotel agent uses Tortoise ORM to manage room availability in a SQLite database. On startup, the database is initialized, and the room availability is set. The agent processes room booking requests and updates the database accordingly.

```python
from uagents import Agent, Context
from tortoise import Tortoise
from models import Availability, RoomRequest, RoomResponse

HOTEL_SEED = "put_hotel_seed_phrase_here"

hotel = Agent(
    name="hotel",
    port=8001,
    seed=HOTEL_SEED,
    endpoint=["http://127.0.0.1:8001/submit"],
)

print(f"hotel's agent address: {hotel.address}")

@hotel.on_event("startup")
async def startup(_ctx: Context):
    await Tortoise.init(
        db_url="sqlite://db.sqlite3", modules={"models": ["models"]}
    )
    await Tortoise.generate_schemas()
    await Availability.create(
        room_available=True,
        min_price=50,
    )

@hotel.on_event("shutdown")
async def shutdown(_ctx: Context):
    await Tortoise.close_connections()

@hotel.on_message(model=RoomRequest)
async def message_handler(ctx: Context, sender: str, msg: RoomRequest):
    availability = await Availability.first()
    success = False
    if availability.room_available:
        ctx.logger.info(f"Room available, attempting to book")
        if availability.min_price <= msg.max_price:
            success = True
            ctx.logger.info(f"Offer of ${msg.max_price} accepted!")
            availability.room_available = False
            await availability.save()
        else:
            ctx.logger.info(f"Offer of ${msg.max_price} was too low, won't accept")
    else:
        ctx.logger.info(f"Room unavailable")
    await ctx.send(sender, RoomResponse(success=success))

if __name__ == "__main__":
    hotel.run()
```

## Running the Example

To observe the room booking interaction between the guest and hotel agents, run:

```
python hotel.py
```

Add the `HOTEL_ADDRESS` to `guest.py` and the run it:

```
python guest.py
```

These commands starts both agents. The guest agent periodically sends a room booking request to the hotel agent, which processes the request based on room availability and price, and responds accordingly.

## Key Points

- Ensure the guest and hotel agents are configured with appropriate seed phrases and endpoints.
- The hotel agent manages room availability using Tortoise ORM and responds to booking requests based on predefined criteria.
- The guest agent continuously sends booking requests until a successful booking is achieved.

By following this example, you can implement a simple room booking system with distributed agents, demonstrating the potential of agent-based architectures in automating tasks and interactions.