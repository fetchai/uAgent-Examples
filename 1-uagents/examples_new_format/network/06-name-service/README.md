# Name Service Example

![domain:uAgents101](https://img.shields.io/badge/uAgents--101-3D8BD3?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMCAwLjVDMCAwLjIzNDM3NSAwLjIxODc1IDAgMC41IDBIMS41QzEuNzY1NjIgMCAyIDAuMjM0Mzc1IDIgMC41VjEuNUgwVjAuNVpNMCAySDJWNkgwVjJaTTAgNi41SDJWNy41QzIgNy43ODEyNSAxLjc2NTYyIDggMS41IDhIMC41QzAuMjE4NzUgOCAwIDcuNzgxMjUgMCA3LjVWNi41Wk0yLjUgMC41QzIuNSAwLjIzNDM3NSAyLjcxODc1IDAgMyAwSDRDNC4yNjU2MiAwIDQuNSAwLjIzNDM3NSA0LjUgMC41VjEuNUgyLjVWMC41Wk0yLjUgMkg0LjVWNkgyLjVWMlpNMi41IDYuNUg0LjVWNy41QzQuNSA3Ljc4MTI1IDQuMjY1NjIgOCA0IDhIM0MyLjcxODc1IDggMi41IDcuNzgxMjUgMi41IDcuNVY2LjVaTTUuNjcxODggNi4yMDMxMkw1IDMuNjQwNjJWMi4yMzQzOEw2LjU2MjUgMS44MTI1TDcuNTkzNzUgNS42ODc1TDUuNjcxODggNi4yMDMxMlpNNi40Mzc1IDEuMzI4MTJMNSAxLjcxODc1VjAuMTcxODc1TDUuNTYyNSAwLjAzMTI1QzUuODI4MTIgLTAuMDQ2ODc1IDYuMTA5MzggMC4xMDkzNzUgNi4xNzE4OCAwLjM3NUw2LjQzNzUgMS4zMjgxMlpNNS43OTY4OCA2LjY3MTg4TDcuNzE4NzUgNi4xNzE4OEw3Ljk2ODc1IDcuMTI1QzguMDQ2ODggNy4zOTA2MiA3Ljg5MDYyIDcuNjU2MjUgNy42MjUgNy43MzQzOEw2LjY3MTg4IDcuOTg0MzhDNi40MDYyNSA4LjA2MjUgNi4xMjUgNy45MDYyNSA2LjA2MjUgNy42NDA2Mkw1Ljc5Njg4IDYuNjcxODhaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)

Welcome to the Name Service Example! This example guides you through setting up agents to communicate using domain names registered through a Name Service Contract on the ledger. This method allows agents to reach each other not just through specific addresses or endpoints, but via human-readable domain names, enhancing the usability and configurability of agent-based systems.

Before diving into the example, ensure your environment is ready by navigating to your project directory and running:

```
poetry install
poetry shell
```

## Using the Name Service for Agent Communication

### Configuration and Wallet Setup

- **Description**: To register a domain name, an agent needs a wallet with tokens. These tokens are used to perform the registration transaction on the ledger.
- **Example Usage**: Before registering his domain name, Bob uses a `LocalWallet` initialized with a seed phrase and obtains tokens from a faucet (`faucet.get_wealth(my_wallet.address())`). This setup is necessary to interact with the Name Service Contract.

### Registering Domain Names

- **Description**: The Name Service Contract on the ledger allows agents to register domain names that map to their ledger addresses. This setup enables other agents to send messages using these domain names instead of needing to know the precise ledger addresses.
- **Example Usage**: Bob registers the domain name `bob-0.example.agent` through the Name Service Contract using a wallet with tokens. This process involves calling `name_service_contract.register` with Bob's agent information and domain.

### Sending Messages to Domain Names

- **Description**: Once a domain name is registered, other agents can send messages to this name. The system resolves the domain name to the agent's ledger address, ensuring the message is delivered correctly.
- **Example Usage**: Alice sends a message to Bob using his registered domain name `bob-0.example.agent`. This allows Alice to communicate with Bob without knowing his exact ledger address.

## Running the Example

To see how domain name registration and communication work, follow these steps:

1. **Run Bob's Script**: Start with Bob's agent script to register his domain name. Ensure Bob's script includes the wallet setup and the call to register the domain name via the Name Service Contract.
2. **Run Alice's Script**: After Bob's domain name is registered, run Alice's script. Alice sends a message to Bob using his domain name, demonstrating how agents can communicate through registered names.

## Key Points

- Domain name registration is restricted to public domains, with `.agent` being a primary example.
- Agents can use registered domain names to communicate, making it easier to address messages and interact within the agent ecosystem.
- A wallet with tokens is necessary for the registration process, as it involves a ledger transaction.
- This example illustrates a foundational use of the Name Service for agent communication, providing a pathway to more dynamic and flexible agent interactions.

The Name Service Example demonstrates a powerful feature of modern agent-based systems, enabling more intuitive and manageable communication channels between agents.
