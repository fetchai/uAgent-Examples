from uagents import Agent

agent = Agent(name="alice", seed="alice recovery phrase", port=8000, endpoint=["http://127.0.0.1:8000/submit"])

print("uAgent address: ", agent.address)

if __name__ == "__main__":
    agent.run()