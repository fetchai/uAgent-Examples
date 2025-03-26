import time

from client import Client
from communication import POI, Coordinates
from uagents import Context


async def find_pois(
    client: Client,
    ctx: Context,
    query_string: str,
    lat: float,
    lng: float,
    radius_in_m: int,
    limit: int = 20,
    _filter: dict = None,
):
    if not query_string:
        ctx.logger.error("No query string provided")
        return
    pois = []
    next_page = None
    while True:
        # Places API always paginates at 20 entries
        try:
            res = client.places(
                query=query_string,
                location=(lat, lng),
                radius=radius_in_m,
                language="en",
                page_token=next_page,
            )
            pois += res["results"]
            next_page = res["next_page_token"] if "next_page_token" in res else None
            # ctx.logger.info(res)
            ctx.logger.info(f"{len(pois)}/{limit} pois found")
            if not next_page:
                break
            if len(pois) >= limit:
                break
            # wait a bit to not trigger the API rate limit (https://github.com/googlemaps/google-maps-services-python/issues/366)
            time.sleep(2)
        except Exception as e:
            ctx.logger.error(e)
            break

    if pois:
        pois_result_list = []
        for p in pois:
            if len(pois_result_list) > limit:
                break
            res = client.place(
                place_id=p["place_id"],
                fields=["address_component"],
                language="en",
            )

            addr_comp = res["result"]["address_components"] or None
            if addr_comp:
                addr = {}
                for e in addr_comp:
                    addr[e["types"][0]] = e["long_name"]

            pois_result_list.append(
                POI(
                    placekey=p["place_id"] or "",
                    location_name=p["name"] or "",
                    location=Coordinates(
                        latitude=p["geometry"]["location"]["lat"],
                        longitude=p["geometry"]["location"]["lng"],
                    ),
                    address=p["formatted_address"] or "",
                    city=addr["administrative_area_level_2"]
                    if "administrative_area_level_2" in addr
                    else "",
                    region=addr["administrative_area_level_1"]
                    if "administrative_area_level_1" in addr
                    else "",
                    postal_code=addr["postal_code"] if "postal_code" in addr else "",
                    iso_country_code=addr["locality"] if "locality" in addr else "",
                )
            )
        return pois_result_list
    return []
