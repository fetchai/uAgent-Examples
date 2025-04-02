import os
import requests

from uagents import Model, Field

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY is None:
    raise ValueError("You need to provide an API key for Google Geocode")


class GeolocationRequest(Model):
    address: str = Field(
        description="Physical address (location)", 
    )

class GeolocationResponse(Model):
    latitude: float
    longitude: float


async def find_coordinates(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": GOOGLE_API_KEY}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)

        data = response.json()

        # Check if results are available in the response
        if "results" in data:
            return {
                "latitude": data["results"][0]["geometry"]["location"]["lat"],
                "longitude": data["results"][0]["geometry"]["location"]["lng"],
            }

        return {"error": "Address not found in the response."}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request failed: {str(req_err)}"}
    except Exception as err:
        return {"error": f"An unexpected error occurred: {str(err)}"}