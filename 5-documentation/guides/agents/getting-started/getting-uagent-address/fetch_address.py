from uagents import Agent

agent = Agent(name="alice", seed="alice recovery phrase", port=8000, endpoint=["http://127.0.0.1:8000/submit"])

print("Fetch network address: ", agent.wallet.address())

if __name__ == "__main__":
    agent.run()