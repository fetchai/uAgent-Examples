# Mailbox Agents Example

![domain:uAgents101](https://img.shields.io/badge/uAgents--101-3D8BD3?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMCAwLjVDMCAwLjIzNDM3NSAwLjIxODc1IDAgMC41IDBIMS41QzEuNzY1NjIgMCAyIDAuMjM0Mzc1IDIgMC41VjEuNUgwVjAuNVpNMCAySDJWNkgwVjJaTTAgNi41SDJWNy41QzIgNy43ODEyNSAxLjc2NTYyIDggMS41IDhIMC41QzAuMjE4NzUgOCAwIDcuNzgxMjUgMCA3LjVWNi41Wk0yLjUgMC41QzIuNSAwLjIzNDM3NSAyLjcxODc1IDAgMyAwSDRDNC4yNjU2MiAwIDQuNSAwLjIzNDM3NSA0LjUgMC41VjEuNUgyLjVWMC41Wk0yLjUgMkg0LjVWNkgyLjVWMlpNMi41IDYuNUg0LjVWNy41QzQuNSA3Ljc4MTI1IDQuMjY1NjIgOCA0IDhIM0MyLjcxODc1IDggMi41IDcuNzgxMjUgMi41IDcuNVY2LjVaTTUuNjcxODggNi4yMDMxMkw1IDMuNjQwNjJWMi4yMzQzOEw2LjU2MjUgMS44MTI1TDcuNTkzNzUgNS42ODc1TDUuNjcxODggNi4yMDMxMlpNNi40Mzc1IDEuMzI4MTJMNSAxLjcxODc1VjAuMTcxODc1TDUuNTYyNSAwLjAzMTI1QzUuODI4MTIgLTAuMDQ2ODc1IDYuMTA5MzggMC4xMDkzNzUgNi4xNzE4OCAwLjM3NUw2LjQzNzUgMS4zMjgxMlpNNS43OTY4OCA2LjY3MTg4TDcuNzE4NzUgNi4xNzE4OEw3Ljk2ODc1IDcuMTI1QzguMDQ2ODggNy4zOTA2MiA3Ljg5MDYyIDcuNjU2MjUgNy42MjUgNy43MzQzOEw2LjY3MTg4IDcuOTg0MzhDNi40MDYyNSA4LjA2MjUgNi4xMjUgNy45MDYyNSA2LjA2MjUgNy42NDA2Mkw1Ljc5Njg4IDYuNjcxODhaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)

Welcome to the Mailbox Agents example! This guide explains how to set up mailbox agents for communication within the Agentverse. The Agentverse Mailroom offers a solution that allows agents to communicate with each other seamlessly, even when one or more agents are not continuously running. This is particularly useful for interactions that do not require immediate responses or for systems where agents operate intermittently.

Before you begin, navigate to your project's directory and prepare your environment:

```
poetry install
poetry shell
```

## Key Concepts

### Agentverse Mailroom

- **Description**: The Agentverse Mailroom facilitates the creation of mailboxes for agents. These mailboxes enable two-way communication between local and Agentverse agents, functioning even when agents are offline. This ensures that messages are not lost and can be retrieved and processed when the agent is active.
- **Example Usage**: Both Alice and Bob agents are configured with mailboxes hosted by the Agentverse Mailroom. This setup allows them to exchange messages reliably, regardless of their operational state.

### Setting Up Mailboxes

- **Process**:
  1. **Obtain Agent Address**: First, determine your agent's address by running the agent script with your seed phrase (uniqueness is crucial for new mailbox creation). The address will be printed to the console.
  2. **Create Mailbox**: Visit [agentverse.ai](https://agentverse.ai) and login, click on the Mailroom section, and create a new mailbox using your agent's address. During this process, you'll receive a unique mailbox key, copy it.
  3. **Configure Script**: Insert the obtained mailbox key into your agent's script in the `mailbox` field, formatted as `AGENT_MAILBOX_KEY`.

### Mailbox Communication

- **Description**: Once mailboxes are configured, agents can send and receive messages through these mailboxes. This setup is particularly useful for asynchronous communication patterns, where agents do not need to respond in real-time.
- **Example Usage**: Bob periodically sends a message to Alice. Alice, through her mailbox, receives the message and can respond when active. Both agents use the `@on_message` decorator to handle incoming messages and can reply using the `ctx.send` method.

## Running the Example

To see mailbox communication in action, follow these steps:

1. **Run Alice or Bob**: Start by running one of the agent scripts to obtain the agent's address.
2. **Create Mailbox**: With the agent's address, create a mailbox on the Agentverse Mailroom and obtain your mailbox key.
3. **Configure and Run the Other Agent**: Configure the other agent with the mailbox key and the first agent's address, then run the script.

By running both agents with properly configured mailboxes, you'll observe how messages are exchanged between Alice and Bob, showcasing the mailbox functionality.