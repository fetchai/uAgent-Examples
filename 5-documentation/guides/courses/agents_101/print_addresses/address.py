from uagents import Agent

agent = Agent(name="alice")

print("uAgent address: ", agent.address)
print("Fetch network address: ", agent.wallet.address())