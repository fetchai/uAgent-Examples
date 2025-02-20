# Bureau Interaction Example

![domain:uAgents101](https://img.shields.io/badge/uAgents--101-3D8BD3?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMCAwLjVDMCAwLjIzNDM3NSAwLjIxODc1IDAgMC41IDBIMS41QzEuNzY1NjIgMCAyIDAuMjM0Mzc1IDIgMC41VjEuNUgwVjAuNVpNMCAySDJWNkgwVjJaTTAgNi41SDJWNy41QzIgNy43ODEyNSAxLjc2NTYyIDggMS41IDhIMC41QzAuMjE4NzUgOCAwIDcuNzgxMjUgMCA3LjVWNi41Wk0yLjUgMC41QzIuNSAwLjIzNDM3NSAyLjcxODc1IDAgMyAwSDRDNC4yNjU2MiAwIDQuNSAwLjIzNDM3NSA0LjUgMC41VjEuNUgyLjVWMC41Wk0yLjUgMkg0LjVWNkgyLjVWMlpNMi41IDYuNUg0LjVWNy41QzQuNSA3Ljc4MTI1IDQuMjY1NjIgOCA0IDhIM0MyLjcxODc1IDggMi41IDcuNzgxMjUgMi41IDcuNVY2LjVaTTUuNjcxODggNi4yMDMxMkw1IDMuNjQwNjJWMi4yMzQzOEw2LjU2MjUgMS44MTI1TDcuNTkzNzUgNS42ODc1TDUuNjcxODggNi4yMDMxMlpNNi40Mzc1IDEuMzI4MTJMNSAxLjcxODc1VjAuMTcxODc1TDUuNTYyNSAwLjAzMTI1QzUuODI4MTIgLTAuMDQ2ODc1IDYuMTA5MzggMC4xMDkzNzUgNi4xNzE4OCAwLjM3NUw2LjQzNzUgMS4zMjgxMlpNNS43OTY4OCA2LjY3MTg4TDcuNzE4NzUgNi4xNzE4OEw3Ljk2ODc1IDcuMTI1QzguMDQ2ODggNy4zOTA2MiA3Ljg5MDYyIDcuNjU2MjUgNy42MjUgNy43MzQzOEw2LjY3MTg4IDcuOTg0MzhDNi40MDYyNSA4LjA2MjUgNi4xMjUgNy45MDYyNSA2LjA2MjUgNy42NDA2Mkw1Ljc5Njg4IDYuNjcxODhaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)

Welcome to the Bureau Interaction example! This guide demonstrates how a `Bureau` can host multiple agents, allowing them to interact and simulate economic transactions on a network. Each agent is initialized with a unique seed to secure their identity and wallet on the blockchain. This setup facilitates complex simulations with numerous agents interacting in a dynamic environment. Before proceeding, navigate to the example directory and set up your environment with:

```
poetry install
poetry shell
```


## Key Concepts

### Multiple Agent Hosting with Bureau

- **Description**: This example showcases a `Bureau` that manages multiple agents. The Bureau acts as a central node where each agent is registered and managed, facilitating interactions and transactions among them.
- **Example Usage**: Agents such as Alice, Bob, Charles, Diana, Ean, and Fabian are registered in the Bureau. Each agent has unique characteristics like minimum acceptable prices for transactions.

### Agent Uniqueness with Seeds

- **Description**: Agents are initialized with unique seeds, which are essential for creating secure and identifiable wallets on the blockchain. This feature ensures that transactions are secure and that they occur between the correct parties.
- **Example Usage**: Each agent, is initialized with a `seed` linked to distinct identities.

### Inter-agent Communication and Transactions

- **Description**: Agents communicate using a defined protocol (`seller_protocol`) where they can send and respond to offers based on predefined minimum prices.
- **Example Usage**: Alice might send an offer to Bob, and if the offer meets or exceeds Bob's minimum price, Bob will accept the offer.

## Running the Simulation

To observe the agents' interactions within the Bureau, follow these steps:

### 1. Start the Bureau and Agents
- Navigate to the `seller.py` directory.
- Run the command:

```
python sellers.py
```
- Each agent's address is printed at startup. Copy these addresses for further interactions.

### 2. Interact with Agents
- Open the file `buyer.py`.
- Paste the copied addresses into the specified location in the file to set up communication links between buyers and sellers.
- Inside the directory, run the command:

```
python buyer.py
```


Following these instructions will initiate the agents, and they will start to interact based on the offers sent and received. Observing the logs will provide insight into the negotiation process and the transactions executed.

## Experimentation

This example lays the groundwork for more complex simulations involving multiple agents. Consider modifying the agents' minimum prices, changing the intervals of offer submissions, or adding more agents to simulate a more dynamic economic environment.
