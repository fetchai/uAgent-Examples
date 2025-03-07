# Protocol Broadcast

![domain:uAgents101](https://img.shields.io/badge/uAgents--101-3D8BD3?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMCAwLjVDMCAwLjIzNDM3NSAwLjIxODc1IDAgMC41IDBIMS41QzEuNzY1NjIgMCAyIDAuMjM0Mzc1IDIgMC41VjEuNUgwVjAuNVpNMCAySDJWNkgwVjJaTTAgNi41SDJWNy41QzIgNy43ODEyNSAxLjc2NTYyIDggMS41IDhIMC41QzAuMjE4NzUgOCAwIDcuNzgxMjUgMCA3LjVWNi41Wk0yLjUgMC41QzIuNSAwLjIzNDM3NSAyLjcxODc1IDAgMyAwSDRDNC4yNjU2MiAwIDQuNSAwLjIzNDM3NSA0LjUgMC41VjEuNUgyLjVWMC41Wk0yLjUgMkg0LjVWNkgyLjVWMlpNMi41IDYuNUg0LjVWNy41QzQuNSA3Ljc4MTI1IDQuMjY1NjIgOCA0IDhIM0MyLjcxODc1IDggMi41IDcuNzgxMjUgMi41IDcuNVY2LjVaTTUuNjcxODggNi4yMDMxMkw1IDMuNjQwNjJWMi4yMzQzOEw2LjU2MjUgMS44MTI1TDcuNTkzNzUgNS42ODc1TDUuNjcxODggNi4yMDMxMlpNNi40Mzc1IDEuMzI4MTJMNSAxLjcxODc1VjAuMTcxODc1TDUuNTYyNSAwLjAzMTI1QzUuODI4MTIgLTAuMDQ2ODc1IDYuMTA5MzggMC4xMDkzNzUgNi4xNzE4OCAwLjM3NUw2LjQzNzUgMS4zMjgxMlpNNS43OTY4OCA2LjY3MTg4TDcuNzE4NzUgNi4xNzE4OEw3Ljk2ODc1IDcuMTI1QzguMDQ2ODggNy4zOTA2MiA3Ljg5MDYyIDcuNjU2MjUgNy42MjUgNy43MzQzOEw2LjY3MTg4IDcuOTg0MzhDNi40MDYyNSA4LjA2MjUgNi4xMjUgNy45MDYyNSA2LjA2MjUgNy42NDA2Mkw1Ljc5Njg4IDYuNjcxODhaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)

Welcome to the Protocol Broadcast example! This guide focuses on a specific example that demonstrates how to broadcast messages to agents sharing the same protocol within a distributed agent system. This capability is pivotal for scenarios where a message needs to be sent to multiple agents simultaneously, such as updates, or requests for information.

To prepare for running the example, ensure you're in the proper directory and have configured your environment with the necessary dependencies:

```
poetry install
poetry shell
```

## Broadcasting Messages with Protocols

### Defining a Shared Protocol

- **Description**: A shared protocol specifies a common communication format and procedure that participating agents agree upon. It ensures that messages are understood and processed uniformly across different agents.
- **Example Usage**: The `hello_protocol` is defined with a simple `Request` and `Response` model. Agents using this protocol can send a greeting request and expect a greeting response.

### Including Protocols in Agents

- **Description**: For an agent to participate in protocol-based communication, it must include the protocol within its definition. This inclusion enables the agent to understand and respond to messages formatted according to the protocol.
- **Example Usage**: Alice and Bob include the `hello_protocol`, making them capable of receiving and responding to broadcast requests sent using this protocol.

### Broadcasting Messages

- **Description**: Broadcasting refers to sending a message to all agents that are capable of understanding it, based on the shared protocol. This is done without specifying individual recipients, allowing for efficient group communication.
- **Example Usage**: Charles periodically broadcasts a greeting using `hello_protocol`. All agents that have included this protocol (Alice and Bob) will receive and respond to the greeting.

## Running the Example

To observe protocol-based broadcasting in action, run:

```
python main.py
```


This command starts the bureau, initializing all three agents. Charles periodically broadcasts a greeting to Alice and Bob, who respond to each greeting, showcasing the broadcasting functionality.

## Key Points

- Ensure that all agents meant to communicate share the same protocol by including it in their definitions.
- Use broadcasting for scenarios where a message needs to be sent to multiple agents without specifying each recipient.

By following this example, you can implement efficient and scalable communication patterns in distributed agent systems, leveraging the power of protocol broadcasting.
