# Flights Retriever Agent

![domain:travel](https://img.shields.io/badge/travel-3D8BD3?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iOSIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOSA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNNy41MzEyNSAzQzguMDYyNSAzIDkgMy40NTMxMiA5IDRDOSA0LjU2MjUgOC4wNjI1IDUgNy41MzEyNSA1SDUuNzAzMTJMNC4xNDA2MiA3Ljc1QzQuMDQ2ODggNy45MDYyNSAzLjg3NSA4IDMuNzAzMTIgOEgyLjgyODEyQzIuNjU2MjUgOCAyLjUzMTI1IDcuODQzNzUgMi41NzgxMiA3LjY4NzVMMy4zNDM3NSA1SDEuNzVMMS4wNjI1IDUuOTA2MjVDMS4wMTU2MiA1Ljk2ODc1IDAuOTUzMTI1IDYgMC44NzUgNkgwLjIxODc1QzAuMDkzNzUgNiAwIDUuOTA2MjUgMCA1Ljc4MTI1QzAgNS43NjU2MiAwIDUuNzUgMCA1LjczNDM4TDAuNSA0TDAgMi4yODEyNUMwIDIuMjY1NjIgMCAyLjI1IDAgMi4yMTg3NUMwIDIuMTA5MzggMC4wOTM3NSAyIDAuMjE4NzUgMkgwLjg3NUMwLjk1MzEyNSAyIDEuMDE1NjIgMi4wNDY4OCAxLjA2MjUgMi4xMDkzOEwxLjc1IDNIMy4zNDM3NUwyLjU3ODEyIDAuMzI4MTI1QzIuNTMxMjUgMC4xNzE4NzUgMi42NTYyNSAwIDIuODI4MTIgMEgzLjcwMzEyQzMuODc1IDAgNC4wNDY4OCAwLjEwOTM3NSA0LjE0MDYyIDAuMjY1NjI1TDUuNzAzMTIgM0g3LjUzMTI1WiIgZmlsbD0id2hpdGUiLz4KPC9zdmc+Cg==)
[![link to source code](https://img.shields.io/badge/Source%20Code-E8ECF1?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNNCAwLjA5ODk5OUMxLjc5IDAuMDk4OTk5IDAgMS44OSAwIDQuMDk5QzAgNS44NjY2NyAxLjE0NiA3LjM2NTY2IDIuNzM1IDcuODk0QzIuOTM1IDcuOTMxNjYgMy4wMDgzMyA3LjgwOCAzLjAwODMzIDcuNzAxNjZDMy4wMDgzMyA3LjYwNjY2IDMuMDA1IDcuMzU1IDMuMDAzMzMgNy4wMjE2N0MxLjg5MDY3IDcuMjYzIDEuNjU2IDYuNDg1IDEuNjU2IDYuNDg1QzEuNDc0IDYuMDIzMzMgMS4yMTEgNS45IDEuMjExIDUuOUMwLjg0ODY2NyA1LjY1MiAxLjIzOSA1LjY1NyAxLjIzOSA1LjY1N0MxLjY0MDY3IDUuNjg1IDEuODUxNjcgNi4wNjkgMS44NTE2NyA2LjA2OUMyLjIwODMzIDYuNjgwNjcgMi43ODggNi41MDQgMy4wMTY2NyA2LjQwMTY2QzMuMDUyNjcgNi4xNDMgMy4xNTU2NyA1Ljk2NjY3IDMuMjcgNS44NjY2N0MyLjM4MTY3IDUuNzY2NjcgMS40NDggNS40MjI2NyAxLjQ0OCAzLjg5QzEuNDQ4IDMuNDUzMzMgMS42MDMgMy4wOTY2NyAxLjg1OTY3IDIuODE2NjdDMS44MTQ2NyAyLjcxNTY3IDEuNjc5NjcgMi4zMDkgMS44OTQ2NyAxLjc1OEMxLjg5NDY3IDEuNzU4IDIuMjI5NjcgMS42NTA2NyAyLjk5NDY3IDIuMTY4QzMuMzE0NjcgMi4wNzkgMy42NTQ2NyAyLjAzNSAzLjk5NDY3IDIuMDMzQzQuMzM0NjcgMi4wMzUgNC42NzQ2NyAyLjA3OSA0Ljk5NDY3IDIuMTY4QzUuNzU0NjcgMS42NTA2NyA2LjA4OTY3IDEuNzU4IDYuMDg5NjcgMS43NThDNi4zMDQ2NyAyLjMwOSA2LjE2OTY3IDIuNzE1NjcgNi4xMjk2NyAyLjgxNjY3QzYuMzg0NjcgMy4wOTY2NyA2LjUzOTY3IDMuNDUzMzMgNi41Mzk2NyAzLjg5QzYuNTM5NjcgNS40MjY2NyA1LjYwNDY3IDUuNzY1IDQuNzE0NjcgNS44NjMzM0M0Ljg1NDY3IDUuOTgzMzMgNC45ODQ2NyA2LjIyODY2IDQuOTg0NjcgNi42MDMzM0M0Ljk4NDY3IDcuMTM4NjYgNC45Nzk2NyA3LjU2ODY3IDQuOTc5NjcgNy42OTg2N0M0Ljk3OTY3IDcuODAzNjcgNS4wNDk2NyA3LjkyODY3IDUuMjU0NjcgNy44ODg2N0M2Ljg1NSA3LjM2NCA4IDUuODY0IDggNC4wOTlDOCAxLjg5IDYuMjA5IDAuMDk4OTk5IDQgMC4wOTg5OTlaIiBmaWxsPSIjNTU2NTc4Ii8%2BCjwvc3ZnPgo%3D)](https://github.com/fetchai/uAgent-Examples/tree/main/6-deployed-agents/travel/flights-retriever-agent)
[![live](https://img.shields.io/badge/Live-8A2BE2?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEwIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI%2BCjxwYXRoIGQ9Ik0yLjI1IDcuNUMxIDcuNSAwIDYuNSAwIDUuMjVDMCA0LjI4MTI1IDAuNjI1IDMuNDM3NSAxLjUgMy4xNDA2MkMxLjUgMy4wOTM3NSAxLjUgMy4wNDY4OCAxLjUgM0MxLjUgMS42MjUgMi42MDkzOCAwLjUgNCAwLjVDNC45MjE4OCAwLjUgNS43MzQzOCAxLjAxNTYyIDYuMTU2MjUgMS43NjU2MkM2LjM5MDYyIDEuNTkzNzUgNi42ODc1IDEuNSA3IDEuNUM3LjgyODEyIDEuNSA4LjUgMi4xNzE4OCA4LjUgM0M4LjUgMy4yMDMxMiA4LjQ1MzEyIDMuMzc1IDguMzkwNjIgMy41NDY4OEM5LjMxMjUgMy43MzQzOCAxMCA0LjU0Njg4IDEwIDUuNUMxMCA2LjYwOTM4IDkuMDkzNzUgNy41IDggNy41SDIuMjVaTTYuNzY1NjIgMy43NjU2MkM2LjkwNjI1IDMuNjI1IDYuOTA2MjUgMy4zOTA2MiA2Ljc2NTYyIDMuMjVDNi42MDkzOCAzLjA5Mzc1IDYuMzc1IDMuMDkzNzUgNi4yMzQzOCAzLjI1TDQuNSA0Ljk4NDM4TDMuNzY1NjIgNC4yNUMzLjYwOTM4IDQuMDkzNzUgMy4zNzUgNC4wOTM3NSAzLjIzNDM4IDQuMjVDMy4wNzgxMiA0LjM5MDYyIDMuMDc4MTIgNC42MjUgMy4yMzQzOCA0Ljc2NTYyTDQuMjM0MzggNS43NjU2MkM0LjM3NSA1LjkyMTg4IDQuNjA5MzggNS45MjE4OCA0Ljc2NTYyIDUuNzY1NjJMNi43NjU2MiAzLjc2NTYyWiIgZmlsbD0id2hpdGUiLz4KPC9zdmc%2BCg%3D%3D)](https://agentverse.ai/agents/details/agent1qfzwqwnqcyqrr8fqdnsu5sac45jl8je53mrrncrzxwlrwa55hgu0vu40es7/profile)

This agent is designed to provide all available **one-way direct flights** based on the specific dates, cities and number of people provided by the user.

It uses the RapidAPI's "Air Scraper" API ([sky-scrapper](https://rapidapi.com/apiheya/api/sky-scrapper)) to access flight data.

It returns the prices in the requested currency.

## Example input

```python
FlightsSearchRequest(
    origin="EDI", # Edinburgh, Scotland
    destination="BOS", # Boston, USA
    date="2024-10-24T10:20", # datetime format
    persons=2,
    currency="GBP" # Currency, ISO 4217, in which you want to get information back
)
```

## Example output

The agent returns all the direct flights that matches the user requirements.

```python
FlightsSearchResponse(
    flights=[
        Flight(
            price=3703.76,
            price_formatted="£3,704",
            origin="Edinburgh",
            destination="Boston Logan International",
            departure_time="2024-10-24T10:35:00",
            arrival_time="2024-10-24T12:50:00",
            airline="Air France",
        ),
        Flight(
            price=3703.76,
            price_formatted="£3,704",
            origin="Edinburgh",
            destination="Boston Logan International",
            departure_time="2024-10-24T10:35:00",
            arrival_time="2024-10-24T12:50:00",
            airline="KLM",
        ),
        Flight(
            price=3703.76,
            price_formatted="£3,704",
            origin="Edinburgh",
            destination="Boston Logan International",
            departure_time="2024-10-24T10:35:00",
            arrival_time="2024-10-24T12:50:00",
            airline="Virgin Atlantic",
        ),
        Flight(
            price=3703.76,
            price_formatted="£3,704",
            origin="Edinburgh",
            destination="Boston Logan International",
            departure_time="2024-10-24T10:35:00",
            arrival_time="2024-10-24T12:50:00",
            airline="Delta",
        ),
    ]
)
```

## Usage Example

```python
from datetime import datetime
from typing import List

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
    flights: List[Flight]


agent = Agent()

flights_agent_address = "{{ .Agent.Address }}"


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

```

### Local Agent

1. Install the necessary packages:

   ```bash
    pip install uagents
   ```

2. To interact with this agent from a local agent instead, replace `agent = Agent()` in the above with:

   ```python
   agent = Agent(
       name="user",
       endpoint="http://localhost:8000/submit",
   )
   ```

3. Run the agent:
   ```bash
   python agent.py
   ```
