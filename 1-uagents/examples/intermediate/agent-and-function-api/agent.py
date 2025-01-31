import requests
from ai_engine import UAgentResponse, UAgentResponseType
from uagents import Agent, Context, Model, Protocol


class Coordinates(Model):
    location: str


# First generate a secure seed phrase (e.g. https://pypi.org/project/mnemonic/)
SEED_PHRASE = "put_your_seed_phrase_here"

# Now go to https://agentverse.ai, register your agent in the Mailroom by providing the address you just copied.
# Then, copy the agent's mailbox key and insert it here below inline
AGENT_MAILBOX_KEY = "put_your_AGENT_MAILBOX_KEY_here"

# Now your agent is ready to join the agentverse!
location_agent = Agent(
    name="location_agent",
    seed=SEED_PHRASE,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)


# Copy the address shown below
print(f"Your agent's address is: {location_agent.address}")

location_protocol = Protocol("Location Coordinates")


async def location_coordinates(latitude, longitude):
    url = "https://geocoding-by-api-ninjas.p.rapidapi.com/v1/reversegeocoding"
    querystring = {"lat": latitude, "lon": longitude}

    headers = {
        "X-RapidAPI-Key": "YOUR_API_KEY",
        "X-RapidAPI-Host": "geocoding-by-api-ninjas.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring, timeout=5)

    data = response.json()[0]["name"]

    return data


@location_protocol.on_message(model=Coordinates, replies=UAgentResponse)
async def location_coordinates_calculator(ctx: Context, sender: str, msg: Coordinates):
    ctx.logger.info(msg.location)
    latitude, longitude = map(str.strip, msg.location.split(","))
    city = location_coordinates(latitude, longitude)
    ctx.logger.info(city)
    message = city
    await ctx.send(
        sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL)
    )


location_agent.include(location_protocol)

location_agent.run()
