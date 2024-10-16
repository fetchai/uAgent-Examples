# Import the required libraries and modules
from cosmpy.aerial.client import LedgerClient, NetworkConfig  # Required to establish a connection to the network
from cosmpy.aerial.faucet import FaucetApi  # Required to fund Alice's wallet if she has a 0 balance
from cosmpy.aerial.wallet import LocalWallet  # Required to create Alice and Bob's local wallets


def main():
    """Run main."""
    # Create Alice and Bob's wallets
    alice = LocalWallet.generate()
    bob = LocalWallet.generate()

    # Establish a connection to the testnet
    ledger = LedgerClient(NetworkConfig.fetchai_stable_testnet())
    faucet_api = FaucetApi(NetworkConfig.fetchai_stable_testnet())

    # Query Alice's Balance
    alice_balance = ledger.query_bank_balance(bob.address())

    # Should alice have no funds in her wallet, add funds
    while alice_balance < (10 ** 18):
        print("Providing wealth to alice...")
        faucet_api.get_wealth(alice.address())
        alice_balance = ledger.query_bank_balance(alice.address())

    # Print Alice and Bob's getting-uagent-address and balances
    print(
        f"Alice Address: {alice.address()} Balance: {ledger.query_bank_balance(alice.address())}"
    )

    print(
        f"Bob   Address: {bob.address()} Balance: {ledger.query_bank_balance(bob.address())}"
    )

    # Broadcast the transaction and print the outputs on the terminal
    tx = ledger.send_tokens(bob.address(), 10, "atestfet", alice)
    print(f"TX {tx.tx_hash} waiting to complete...")

    tx.wait_to_complete()

    print(f"TX {tx.tx_hash} waiting to complete...done")

    print(
        f"Alice Address: {alice.address()} Balance: {ledger.query_bank_balance(alice.address())}"
    )

    print(
        f"Bob   Address: {bob.address()} Balance: {ledger.query_bank_balance(bob.address())}"
    )


if __name__ == "__main__":
    main()