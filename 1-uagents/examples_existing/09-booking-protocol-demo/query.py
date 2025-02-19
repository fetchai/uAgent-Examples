import asyncio

from protocols.query import GetTotalQueries, TotalQueries

from uagents.envelope import Envelope
from uagents.query import query

RESTAURANT_ADDRESS = "agent1qfpqn9jhvp9cg33f27q6jvmuv52dgyg9rfuu37rmxrletlqe7lewwjed5gy"


async def main():
    response = await query(RESTAURANT_ADDRESS, GetTotalQueries())
    if isinstance(response, Envelope):
        msg = TotalQueries.parse_raw(response.decode_payload())
        print(f"Query response: {msg.json()}\n\n")
    else:
        print(f"Error: {response}")


if __name__ == "__main__":
    asyncio.run(main())
