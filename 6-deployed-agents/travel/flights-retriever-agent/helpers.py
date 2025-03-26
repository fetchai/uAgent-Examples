import logging
import os
from http import HTTPStatus

import requests
from requests import Response
from schemas import Flight, FlightsSearchRequest
from tenacity import retry, stop_after_attempt, wait_exponential
from uagents.storage import StorageAPI

RAPIDAPI_API_KEY = os.environ.get("RAPIDAPI_API_KEY")

assert (
    RAPIDAPI_API_KEY
), "RAPIDAPI_API_KEY environment variable is missing from .secrets file."

SEARCH_AIRPORT = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchAirport"
RAPIDAPI_SKY_SCRAPPER_URL = "https://sky-scrapper.p.rapidapi.com"
RAPIDAPI_SKY_SCRAPPER_ENDPOINTS: dict[str, str] = {
    "get_all_flights": f"{RAPIDAPI_SKY_SCRAPPER_URL}/api/v2/flights/searchFlightsComplete"
}

HEADERS = {
    "content-type": "application/json",
    "X-RapidAPI-Key": RAPIDAPI_API_KEY,
    "X-RapidAPI-Host": "sky-scrapper.p.rapidapi.com",
}


class NotDirectFlightException(Exception):
    pass


@retry(wait=wait_exponential(multiplier=1, min=1, max=5), stop=stop_after_attempt(5))
def _request_get(url: str, query: dict, logger: logging.Logger) -> Response:
    try:
        response: Response = requests.get(
            url, headers=HEADERS, params=query, timeout=30
        )
    except Exception as exc:
        logger.exception(
            f"Some problem at requesting to RapidAPI, we were not able to fetch any data.; \n {exc}"
        )
        raise

    if response.status_code != HTTPStatus.OK:
        logger.error(
            f"Some problem at requesting to RapidAPI, we were not able to fetch any data.\n"
            f"url: {response.request.url}\n"
            f"response code: {response.status_code}\n"
            f"response: {response.text}"
        )

    return response


def get_entity_code(
    logger: logging.Logger, iata: str, storage: StorageAPI
) -> str | None:
    try:
        iata_cache: dict = storage.get("iata_cache") or {}
        if iata in iata_cache:
            return iata_cache[iata]

        response = _request_get(
            url=SEARCH_AIRPORT, query={"query": iata}, logger=logger
        )

        if response.status_code != HTTPStatus.OK:
            logger.info(
                f"get_entity_code failed to call API: {response.status_code}, {response.reason}, {response.json()}"
            )
            return None
        data = response.json()["data"]

        for entry in data:
            if entry["skyId"] == iata:
                iata_cache[iata] = entry["entityId"]
                storage.set("iata_cache", iata_cache)
                return entry["entityId"]
    except Exception as ex:
        logger.exception(f"get_entity_code exception: {ex}")
        return None


def create_direct_flight_from_sky_scrapper_response(itinerary: dict) -> Flight:
    """
    "Itinerary" is just the key name defined by sky-scrapper that has the data of our interest.
    """

    if len(itinerary["legs"][0]["segments"]) > 1:
        raise NotDirectFlightException

    price: float = itinerary["price"]["raw"]
    price_formatted: str = itinerary["price"]["formatted"]
    flight_details = itinerary["legs"][0]  # That list has always just one entry.

    return Flight(
        price=price,
        price_formatted=price_formatted,
        airline=flight_details["carriers"]["marketing"][0]["name"],
        departure_time=flight_details["departure"],
        origin=flight_details["origin"]["name"],
        arrival_time=flight_details["arrival"],
        destination=flight_details["destination"]["name"],
    )


def search_flights(
    logger: logging.Logger, request: FlightsSearchRequest, storage: StorageAPI
) -> dict | None:
    """
    Returns
        dict; The result, the flight itself.
        None; If some error occurred, and/or it has not been processable.
    """
    date = request.date.strftime("%Y-%m-%d")
    origin = get_entity_code(logger=logger, iata=request.origin, storage=storage)
    if origin is None:
        return None

    destination = get_entity_code(
        logger=logger, iata=request.destination, storage=storage
    )
    if destination is None:
        return None

    query = {
        "originSkyId": request.origin,
        "destinationSkyId": request.destination,
        "originEntityId": origin,
        "destinationEntityId": destination,
        "date": date,
        "adults": request.persons,
        "currency": request.currency,
    }
    response = _request_get(
        url=RAPIDAPI_SKY_SCRAPPER_ENDPOINTS["get_all_flights"],
        query=query,
        logger=logger,
    )
    if response.status_code != HTTPStatus.OK:
        logger.info(
            f"search_flights failed to call API: {response.status_code}, {response.reason}"
        )
        return None

    data: dict = response.json()
    if "data" not in data:
        logger.error(
            f"We have received and unexpected response, here it goes:\n {data}"
        )
        return None

    return data["data"]
