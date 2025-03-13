# Protocols Example

![domain:uAgents101](https://img.shields.io/badge/uAgents--101-3D8BD3?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMCAwLjVDMCAwLjIzNDM3NSAwLjIxODc1IDAgMC41IDBIMS41QzEuNzY1NjIgMCAyIDAuMjM0Mzc1IDIgMC41VjEuNUgwVjAuNVpNMCAySDJWNkgwVjJaTTAgNi41SDJWNy41QzIgNy43ODEyNSAxLjc2NTYyIDggMS41IDhIMC41QzAuMjE4NzUgOCAwIDcuNzgxMjUgMCA3LjVWNi41Wk0yLjUgMC41QzIuNSAwLjIzNDM3NSAyLjcxODc1IDAgMyAwSDRDNC4yNjU2MiAwIDQuNSAwLjIzNDM3NSA0LjUgMC41VjEuNUgyLjVWMC41Wk0yLjUgMkg0LjVWNkgyLjVWMlpNMi41IDYuNUg0LjVWNy41QzQuNSA3Ljc4MTI1IDQuMjY1NjIgOCA0IDhIM0MyLjcxODc1IDggMi41IDcuNzgxMjUgMi41IDcuNVY2LjVaTTUuNjcxODggNi4yMDMxMkw1IDMuNjQwNjJWMi4yMzQzOEw2LjU2MjUgMS44MTI1TDcuNTkzNzUgNS42ODc1TDUuNjcxODggNi4yMDMxMlpNNi40Mzc1IDEuMzI4MTJMNSAxLjcxODc1VjAuMTcxODc1TDUuNTYyNSAwLjAzMTI1QzUuODI4MTIgLTAuMDQ2ODc1IDYuMTA5MzggMC4xMDkzNzUgNi4xNzE4OCAwLjM3NUw2LjQzNzUgMS4zMjgxMlpNNS43OTY4OCA2LjY3MTg4TDcuNzE4NzUgNi4xNzE4OEw3Ljk2ODc1IDcuMTI1QzguMDQ2ODggNy4zOTA2MiA3Ljg5MDYyIDcuNjU2MjUgNy42MjUgNy43MzQzOEw2LjY3MTg4IDcuOTg0MzhDNi40MDYyNSA4LjA2MjUgNi4xMjUgNy45MDYyNSA2LjA2MjUgNy42NDA2Mkw1Ljc5Njg4IDYuNjcxODhaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)

Welcome to the Protocols example! This guide delves into the concept of protocols within agents, demonstrating how to define and incorporate them for inter-agent communication. Before proceeding, ensure you navigate to the example directory then run the following commands to set up your environment with the necessary dependencies:

```
poetry install
poetry shell
```


## Key Concepts

### Protocols

- **Description**: A protocol in this context defines a set of rules or procedures for data exchange between agents. By defining a protocol, you establish a structured way for agents to communicate, ensuring they understand each other's messages.
- **Example Usage**: In the example, the `square_protocol` is defined to handle messages related to squaring a number. It specifies the message format for requests and responses, allowing agents to communicate this specific type of information reliably.

### Incorporating Protocols into Agents

- **Description**: Once a protocol is defined, it can be incorporated into an agent. This makes the agent aware of the protocol and enables it to send and receive messages that conform to the protocol's definitions.
- **Example Usage**: Both Alice and Bob agents include the `square_protocol`, which means they can participate in exchanges defined by this protocol, such as sending a number to square and receiving the squared result.

### Agent Seeds

- **Description**: A seed can be used to generate a unique identity for an agent. This is crucial in scenarios where agents need to be distinguishable from each other, for example, in a network of agents communicating over a protocol.
- **Example Usage**: Alice and Bob are given unique seeds (`ALICE_SEED` and `BOB_SEED`), ensuring their identities are distinct in the system.

## Running the Agents

To observe the interaction between the agents, follow these steps:

### 1. Start Agent Bob
- Navigate to the directory named `bob`.
- Run the command:
  ```
  python agent.py 
  ```
- Upon starting, agent bob can print its address using `bob.address`. Make sure to copy this address.

### 2. Start Agent Alice
- Open the file alice/agent.py.
- Paste the copied address of agent bob into the specified location in the file to set up the communication link between Alice and Bob.
- Inside alice directory, run the command:
  ```
  python agent.py
  ```
Following these instructions will initiate agent alice, which will then connect to agent bob using the provided address. You will see logs indicating their communication, you will see logs indicating that Alice is asking Bob what 7 squared is, and Bob responding with the answer. 
## Experimentation

Now that you understand how the protocol works and how it's incorporated into agents, try reversing the roles. Instead of Alice asking Bob to square a number, modify the code to have Bob ask Alice. This change will help you grasp the flexibility of protocols

Protocols are a powerful concept in agent-based systems, enabling structured and reliable communication. By defining a protocol and incorporating it into agents, you create a foundation for complex interactions.
