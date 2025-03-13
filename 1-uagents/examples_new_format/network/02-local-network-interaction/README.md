# Local Network Interactions

![domain:uAgents101](https://img.shields.io/badge/uAgents--101-3D8BD3?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMCAwLjVDMCAwLjIzNDM3NSAwLjIxODc1IDAgMC41IDBIMS41QzEuNzY1NjIgMCAyIDAuMjM0Mzc1IDIgMC41VjEuNUgwVjAuNVpNMCAySDJWNkgwVjJaTTAgNi41SDJWNy41QzIgNy43ODEyNSAxLjc2NTYyIDggMS41IDhIMC41QzAuMjE4NzUgOCAwIDcuNzgxMjUgMCA3LjVWNi41Wk0yLjUgMC41QzIuNSAwLjIzNDM3NSAyLjcxODc1IDAgMyAwSDRDNC4yNjU2MiAwIDQuNSAwLjIzNDM3NSA0LjUgMC41VjEuNUgyLjVWMC41Wk0yLjUgMkg0LjVWNkgyLjVWMlpNMi41IDYuNUg0LjVWNy41QzQuNSA3Ljc4MTI1IDQuMjY1NjIgOCA0IDhIM0MyLjcxODc1IDggMi41IDcuNzgxMjUgMi41IDcuNVY2LjVaTTUuNjcxODggNi4yMDMxMkw1IDMuNjQwNjJWMi4yMzQzOEw2LjU2MjUgMS44MTI1TDcuNTkzNzUgNS42ODc1TDUuNjcxODggNi4yMDMxMlpNNi40Mzc1IDEuMzI4MTJMNSAxLjcxODc1VjAuMTcxODc1TDUuNTYyNSAwLjAzMTI1QzUuODI4MTIgLTAuMDQ2ODc1IDYuMTA5MzggMC4xMDkzNzUgNi4xNzE4OCAwLjM3NUw2LjQzNzUgMS4zMjgxMlpNNS43OTY4OCA2LjY3MTg4TDcuNzE4NzUgNi4xNzE4OEw3Ljk2ODc1IDcuMTI1QzguMDQ2ODggNy4zOTA2MiA3Ljg5MDYyIDcuNjU2MjUgNy42MjUgNy43MzQzOEw2LjY3MTg4IDcuOTg0MzhDNi40MDYyNSA4LjA2MjUgNi4xMjUgNy45MDYyNSA2LjA2MjUgNy42NDA2Mkw1Ljc5Njg4IDYuNjcxODhaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)

Welcome to the Local Network Interactions example! this document details how to set up and run two agents, Alice and Bob, for local network interactions. This example highlights the configuration of ports and endpoints to enable communication between agents running on the same machine but simulating a distributed environment.

To set up your environment for running the examples, navigate to the example directory and execute the following commands:

```
poetry install
poetry shell
```


## Configuration for Local Network Interaction

### Ports and Endpoints

- **Description**: For agents to interact over a local network, each agent must be assigned a unique port and endpoint. The port indicates where the agent is listening for messages, and the endpoint provides a URL for sending messages to the agent.
- **Example Usage**: 
  - Bob is configured to listen on port 8001 and has an endpoint `http://127.0.0.1:8001/submit`. 
  - Alice is set up to use port 8000, with her endpoint being `http://127.0.0.1:8000/submit`.

### Running Bob and Alice Agents

1. **Start Bob**: Run Bob's script first. This initializes Bob on his configured port and prints his address to the terminal.

```
python bob.py
```

Note Bob's address as it is printed in the terminal. This address is needed for Alice to send messages to Bob.

2. **Configure Alice with Bob's Address**: Before running Alice's script, replace `BOB_ADDRESS` in Alice's code with the address you noted from Bob's terminal output. This step is crucial for enabling Alice to correctly send messages to Bob.

3. **Start Alice**: Once Bob's address is configured in Alice's script, run Alice's script. This starts Alice on her configured port, allowing her to send messages to Bob and receive responses.

```
python alice.py
```


## Communication Flow

- Upon running both scripts with the correct configurations, Alice sends a message to Bob every 2 seconds.
- Bob, upon receiving a message from Alice, logs the message and responds with a greeting.
- Alice then receives Bob's response and logs it, demonstrating successful local network interaction between the two agents.

## Key Points

- Ensure that each agent has a unique port and endpoint configured for local network interactions.
- Start the receiving agent (Bob) first to ensure his address is available for configuring the sending agent (Alice).
- Update the sender's (Alice's) code with the receiver's (Bob's) address before starting the sender agent.



## Sending Synchronous Messages

The Synchronous Messages example showcases the ease of sending synchronous messages, which can be essential for applications requiring immediate message delivery and response.

To run the synchronous message sending example, you will need to execute the sync_sender.py script. This script utilizes asyncio to send a synchronous message and wait for a response. Here is a brief explanation of what happens in the script:

- For applications requiring immediate delivery and responses, use the sync_sender.py script.
- It utilizes asyncio to send synchronous messages and awaits responses.
- To use, replace `RECIPIENT_ADDRESS` in the script with Bob's address, and then run:
```
python sync_sender.py
```