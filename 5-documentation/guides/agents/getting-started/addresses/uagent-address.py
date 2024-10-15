from uagents import Agent

agent = Agent(name="alice", seed="alice recovery phrase")

print("uAgent address: ", agent.address)

if __name__ == "__main__":
    agent.run()