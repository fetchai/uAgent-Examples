"""API adapter for the OpenChargeMap API."""

from enum import Enum
from typing import Any, Dict

import requests


class Base(Enum):
    """
    Base URL of the API
    """

    BASE = "https://api.openchargemap.io/v3"


class Endpoint(Enum):
    """
    API endpoints with URLs and arguments

    A route is defined by a tuple of the URL and a list of arguments.
    The arguments are used to fill the URL with the values of the arguments.
    """

    BASE_POI: tuple[str, list[str]] = (
        "/poi",
        [
            "latitude",
            "longitude",
            "distance",
            "distanceunit",
            "maxresults",
            "compact",
            "verbose",
            "client",
        ],
    )
    BASE_REFERENCE_DATA: tuple[str, list[str]] = (
        "/referencedata",
        ["countryid"],
    )


class Unit(Enum):
    KM = "km"
    MILES = "miles"


class OCMAPI:
    """API adapter for the OpenChargeMap API."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.timeout = 10

    def _get_data(
        self,
        endpoint: Endpoint,
        args: dict[str, Any] | None = None,
    ) -> Dict:
        arguments = dict.fromkeys(endpoint.value[1])
        if args:
            arguments.update(**args)
        url = Base[endpoint.name[: len(Base.BASE.name)]].value + endpoint.value[0]
        response = requests.get(
            url=url,
            headers={
                "X-API-Key": self.api_key,
            },
            params=arguments,
            timeout=self.timeout,
        )
        if response.status_code == 200:
            data = response.json()
            return data
        return None

    def get_chargers(
        self,
        latitude: float,
        longitude: float,
        distance: float = 1.0,
        distanceunit: Unit = Unit.KM,
        maxresults: int = 100,
        compact: bool = True,
        verbose: bool = True,
    ) -> list[Dict]:
        """
        Get a list of charging stations in a given area.

        :param latitude: latitude of the center of the area
        :param longitude: longitude of the center of the area
        :param distance: distance in km or miles, defaults to 1.0
        :param distanceunit: unit of the distance, defaults to Unit.KM
        :param maxresults: maximum nr of results, defaults to 100
        :param compact: True removes some extra data, defaults to True
        :param verbose: False removes NULL values, defaults to True
        :return: list of charging stations
        """
        return self._get_data(
            Endpoint.BASE_POI,
            {
                "client": "fetch.ai",
                "latitude": latitude,
                "longitude": longitude,
                "distance": distance,
                "distanceunit": distanceunit,
                "maxresults": maxresults,
                "compact": compact,
                "verbose": verbose,
            },
        )

    def get_reference_data(self, country_id: int | None = None) -> Dict:
        """
        Get reference data for a specific country ID.
        E.g. Germany = 87

        :param country_id: int; country ID
        :return: dict; reference data
        """
        return self._get_data(Endpoint.BASE_REFERENCE_DATA, {"countryid": country_id})
