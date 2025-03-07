# How to use Dialogues

![domain:uAgents101](https://img.shields.io/badge/uAgents--101-3D8BD3?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMCAwLjVDMCAwLjIzNDM3NSAwLjIxODc1IDAgMC41IDBIMS41QzEuNzY1NjIgMCAyIDAuMjM0Mzc1IDIgMC41VjEuNUgwVjAuNVpNMCAySDJWNkgwVjJaTTAgNi41SDJWNy41QzIgNy43ODEyNSAxLjc2NTYyIDggMS41IDhIMC41QzAuMjE4NzUgOCAwIDcuNzgxMjUgMCA3LjVWNi41Wk0yLjUgMC41QzIuNSAwLjIzNDM3NSAyLjcxODc1IDAgMyAwSDRDNC4yNjU2MiAwIDQuNSAwLjIzNDM3NSA0LjUgMC41VjEuNUgyLjVWMC41Wk0yLjUgMkg0LjVWNkgyLjVWMlpNMi41IDYuNUg0LjVWNy41QzQuNSA3Ljc4MTI1IDQuMjY1NjIgOCA0IDhIM0MyLjcxODc1IDggMi41IDcuNzgxMjUgMi41IDcuNVY2LjVaTTUuNjcxODggNi4yMDMxMkw1IDMuNjQwNjJWMi4yMzQzOEw2LjU2MjUgMS44MTI1TDcuNTkzNzUgNS42ODc1TDUuNjcxODggNi4yMDMxMlpNNi40Mzc1IDEuMzI4MTJMNSAxLjcxODc1VjAuMTcxODc1TDUuNTYyNSAwLjAzMTI1QzUuODI4MTIgLTAuMDQ2ODc1IDYuMTA5MzggMC4xMDkzNzUgNi4xNzE4OCAwLjM3NUw2LjQzNzUgMS4zMjgxMlpNNS43OTY4OCA2LjY3MTg4TDcuNzE4NzUgNi4xNzE4OEw3Ljk2ODc1IDcuMTI1QzguMDQ2ODggNy4zOTA2MiA3Ljg5MDYyIDcuNjU2MjUgNy42MjUgNy43MzQzOEw2LjY3MTg4IDcuOTg0MzhDNi40MDYyNSA4LjA2MjUgNi4xMjUgNy45MDYyNSA2LjA2MjUgNy42NDA2Mkw1Ljc5Njg4IDYuNjcxODhaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)

#### Define a pattern (generic dialogue without models)

1. Define the intended behaviour / communication flow as a directed graph.
2. Create a new class inheriting from `Dialogue`.
3. Specify nodes and edges according to the graph.
4. Specify a concrete transition decorator for each transition (=edge).

See `chitchat.py` for an example.

**Note:** The default state represents the state that the agent is in when a dialogue with another agent hasn't been started yet. This state is not shared but exists for each potential dialogue instance with other agents. The default state is included for completeness of the Dialogue graph and has no functional role.

#### Implement a pattern (attach models to transitions)

1. Instantiate a dialogue (e.g., `ChitChatDialogue`) with your agents address.
2. Define message models for each transition defined in the dialogue, according to the needs of your use case.
3. Implement all state transition decorators defined in the dialogue, similarly to the `on_message` handler and register the corresponding models with the respective transitions.

See `agent1.py` and `agent2.py` for an example implementation of the `ChitChatDialogue` defined in `chitchat.py`.

To use the example start `agent1` first, then `agent2` which will initiate the dialogue after 5 seconds. To exit the dialogue press `ctrl + d` on your keyboard.

### Examples

#### Open Dialogue (Agent 1 & 2)

Agent 1 and 2 make use of an implementation of the ChitChat Dialogue in which each step of the graph is exposed to the user. Both agents will be able to communicate as long as both define the same Models for the predefined graph (ChitChatDialogue class).

#### Predefined Dialogue (Agent 3 & 4)

Agent 3 and 4 are given a graph of the same ChitChat Dialogue but most of the interactions are automated and not exposed to the user. Only one interaction to start the dialogue and the cyclic ChitChat message is required to use the graph.
