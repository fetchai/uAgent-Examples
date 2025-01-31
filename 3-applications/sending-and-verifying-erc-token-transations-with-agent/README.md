# sending-and-verifying-token-transations-with-agent

# Web3 Project

This project showcases the integration of the Web3.py library with uAgents to interact with Ethereum smart contracts and manage agent systems. The example highlights initiating a USDC transfer, processing the transaction, and verifying the transaction status through a agent system. This includes demonstrating how uAgents can be used to facilitate token transfers to smart contracts and send funds seamlessly

## Prerequisites

- **Python 3.10+**
- **Poetry** for dependency management
- **ABI.json file** for the contract you want to interact with

## Python Dependencies

The following dependencies are required and managed using Poetry:

- `web3` >= 7.0.0
- `python-dotenv` >= 1.0.1
- `uagents` >= 0.18.0

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd web3-project
   ```

2. Install dependencies using Poetry:
   `poetry install`

3. Setting Up Environment Variables

   ```plaintext
   WEB3_PROVIDER_URL=<Your Web3 Provider URL>
   SENDER_ADDRESS=<Your Sender Address>
   RECEIVER_ADDRESS=<Receiver Address>
   SENDER_PRIVATE_KEY=<Your Private Key>
   USDC_CONTRACT_ADDRESS=<USDC Contract Address>
   AMOUNT=<Amount to Transfer>
   ```

4. Run the example: `python transaction.py`
