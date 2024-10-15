from uagents import Agent

agent = Agent(name="alice", seed="alice recovery phrase")

print("Fetch network address: ", agent.wallet.address())

if __name__ == "__main__":
    agent.run()