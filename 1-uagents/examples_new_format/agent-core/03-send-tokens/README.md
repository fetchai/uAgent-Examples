# Send Tokens Example

![domain:uAgents101](https://img.shields.io/badge/uAgents--101-3D8BD3?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMCAwLjVDMCAwLjIzNDM3NSAwLjIxODc1IDAgMC41IDBIMS41QzEuNzY1NjIgMCAyIDAuMjM0Mzc1IDIgMC41VjEuNUgwVjAuNVpNMCAySDJWNkgwVjJaTTAgNi41SDJWNy41QzIgNy43ODEyNSAxLjc2NTYyIDggMS41IDhIMC41QzAuMjE4NzUgOCAwIDcuNzgxMjUgMCA3LjVWNi41Wk0yLjUgMC41QzIuNSAwLjIzNDM3NSAyLjcxODc1IDAgMyAwSDRDNC4yNjU2MiAwIDQuNSAwLjIzNDM3NSA0LjUgMC41VjEuNUgyLjVWMC41Wk0yLjUgMkg0LjVWNkgyLjVWMlpNMi41IDYuNUg0LjVWNy41QzQuNSA3Ljc4MTI1IDQuMjY1NjIgOCA0IDhIM0MyLjcxODc1IDggMi41IDcuNzgxMjUgMi41IDcuNVY2LjVaTTUuNjcxODggNi4yMDMxMkw1IDMuNjQwNjJWMi4yMzQzOEw2LjU2MjUgMS44MTI1TDcuNTkzNzUgNS42ODc1TDUuNjcxODggNi4yMDMxMlpNNi40Mzc1IDEuMzI4MTJMNSAxLjcxODc1VjAuMTcxODc1TDUuNTYyNSAwLjAzMTI1QzUuODI4MTIgLTAuMDQ2ODc1IDYuMTA5MzggMC4xMDkzNzUgNi4xNzE4OCAwLjM3NUw2LjQzNzUgMS4zMjgxMlpNNS43OTY4OCA2LjY3MTg4TDcuNzE4NzUgNi4xNzE4OEw3Ljk2ODc1IDcuMTI1QzguMDQ2ODggNy4zOTA2MiA3Ljg5MDYyIDcuNjU2MjUgNy42MjUgNy43MzQzOEw2LjY3MTg4IDcuOTg0MzhDNi40MDYyNSA4LjA2MjUgNi4xMjUgNy45MDYyNSA2LjA2MjUgNy42NDA2Mkw1Ljc5Njg4IDYuNjcxODhaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)

Welcome to the Send Tokens example! This guide illustrates how agents can trade tokens on the Fetch.ai blockchain, creating economic interactions within an agent-based system. This example also emphasizes the importance of using seeds for agent identity, as each agent possesses a Fetch wallet tied to its unique identity. Before you begin, make sure to navigate to the example directory and set up your environment with the following commands:

```
poetry install
poetry shell
```

## Key Concepts

### Trading Tokens between Agents

- **Description**: This example demonstrates how agents can send tokens using the Fetch.ai blockchain, showcasing the potential for economic interactions in agent systems. Agents use models to define the structure of payment requests and transaction information, facilitating clear communication about token transfers.
- **Example Usage**: Alice sends a `PaymentRequest` to Bob, specifying the wallet address, amount, and denomination of tokens she requests. Bob, upon receiving this request, sends the specified amount of tokens to Alice's address and informs her of the transaction's hash.

### Agent Uniqueness with Seeds

- **Description**: Each agent is initialized with a unique seed phrase, which is critical for securing and distinguishing their respective Fetch wallets. This uniqueness is essential for economic transactions to ensure that tokens are sent to and from the correct entities.
- **Example Usage**: Alice and Bob are initialized with their respective `ALICE_SEED` and `BOB_SEED`, linking them to distinct wallets on the Fetch.ai blockchain.

### Using `ctx.ledger` for Token Transactions

- **Description**: The context (`ctx`) provides access to the `ledger` object, which agents use to interact with the blockchain. This includes functionalities like sending tokens, checking transaction statuses, and accessing wallet addresses.
- **Example Usage**: Bob uses `ctx.ledger.send_tokens` to transfer tokens to Alice's wallet in response to her payment request. Alice then uses `wait_for_tx_to_complete` with `ctx.ledger` to check the status of the transaction using the transaction hash provided by Bob.

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
Following these instructions will initiate agent alice, which will then connect to agent bob using the provided address. You will see them to communicate and execute token transactions as defined in the example. Observing the logs will show you the payment request from Alice, the transaction initiation by Bob, and the successful transaction confirmation.

## Experimentation

This example sets a foundation for exploring more economic interactions between agents. Consider modifying the amount of tokens requested, experimenting with different intervals for payment requests, or introducing more agents into the system to simulate a more dynamic economic environment.

