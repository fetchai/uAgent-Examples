from typing import Any, Optional

from uagents import Model


class Coordinates(Model):
    latitude: float
    longitude: float


class POIAreaRequest(Model):
    loc_search: Coordinates
    radius_in_m: int
    limit: int = 20
    query_string: str
    filter: dict[str, Any] = {}


class POI(Model):
    placekey: str
    location_name: str
    brands: Optional[list[str]] = None
    top_category: Optional[str] = None
    sub_category: Optional[str] = None
    location: Coordinates
    address: str
    city: str
    region: Optional[str] = None
    postal_code: str
    iso_country_code: str
    metadata: Optional[dict[str, Any]] = None


class POIResponse(Model):
    loc_search: Coordinates
    radius_in_m: int
    data_origin: str
    data: list[POI]