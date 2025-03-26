from datetime import datetime
from typing import List

from uagents import Field, Model


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
