from uagents import Agent, Bureau, Context, Model
from web3 import Web3
from dotenv import load_dotenv
from typing import Optional, Dict
import os
import json
 
load_dotenv()
 
 
provider_url = os.getenv("WEB3_PROVIDER_URL")
sender_address = os.getenv("SENDER_ADDRESS")
sender_private_key = os.getenv("SENDER_PRIVATE_KEY")
deployed_contract_address = os.getenv("DEPLOYED_CONTRACT_ADDRESS")
amount = os.getenv("AMOUNT")
 
 
with open("contract_abi.json") as abi_file:
    proxy_abi = json.load(abi_file)
 
 
w3 = Web3(Web3.HTTPProvider(provider_url))
proxy_contract = w3.eth.contract(address=deployed_contract_address, abi=proxy_abi)
stake_amount = w3.to_wei(amount, "mwei")
 
 
class StakingRequest(Model):
    action: str
    transaction_hash: Optional[str] = None
 
 
class StakingResponse(Model):
    message: str
    transaction_receipt: Optional[Dict] = None
 
 
user_agent = Agent(name="user_agent", seed="user_agent recovery phrase")
stake_agent = Agent(name="stake_agent", seed="stake_agent recovery phrase")
unstake_agent = Agent(name="unstake_agent", seed="unstake_agent recovery phrase")
 
 
def create_receipt_dict(receipt) -> Dict:
    """
    Creates a dictionary from the transaction receipt details.
    Args:
        receipt: The transaction receipt returned by the Web3 `wait_for_transaction_receipt` function.
    Returns:
        A dictionary containing details of the transaction receipt.
    """
    return {
        "transactionHash": receipt.transactionHash.hex(),
        "transactionIndex": receipt.transactionIndex,
        "blockNumber": receipt.blockNumber,
        "blockHash": receipt.blockHash.hex(),
        "cumulativeGasUsed": receipt.cumulativeGasUsed,
        "gasUsed": receipt.gasUsed,
        "status": receipt.status,
    }
 
 
def sign_and_send_transaction(transaction, sender_account):
    """
    Signs and sends a transaction to the blockchain.
    Args:
        transaction: The transaction to be sent.
        sender_account: The account object used to sign the transaction.
    Returns:
        The receipt of the transaction.
    """
    signed_txn = sender_account.sign_transaction(transaction)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    return w3.eth.wait_for_transaction_receipt(tx_hash)
 
 
@user_agent.on_event("startup")
async def handle_user_input(ctx: Context):
    ctx.logger.info(f"*** User Agent startup event triggered. ***")
    action = input("Do you want to 'stake' or 'unstake' tokens? ")
    if action.lower() == "stake":
        await ctx.send(stake_agent.address, StakingRequest(action="stake_tokens"))
    elif action.lower() == "unstake":
        await ctx.send(unstake_agent.address, StakingRequest(action="unstake_tokens"))
    else:
        ctx.logger.info("*** Invalid action. Please enter 'stake' or 'unstake'. ***")
 
 
@user_agent.on_message(model=StakingResponse)
async def user_agent_response_handler(ctx: Context, sender: str, msg: StakingResponse):
    ctx.logger.info(f"*** Received response from {sender}: {msg.message} ***")
    if msg.transaction_receipt is not None:
        ctx.storage.set("receipt", msg.transaction_receipt)
        ctx.logger.info(f"*** Transaction successful: {msg.transaction_receipt} ***")
 
 
@stake_agent.on_message(model=StakingRequest, replies=StakingResponse)
async def stake_handler(ctx: Context, sender: str, msg: StakingRequest):
    sender_account = w3.eth.account.from_key(sender_private_key)
    gas_price = w3.eth.gas_price
    nonce = w3.eth.get_transaction_count(sender_address)
    ctx.logger.info(f"*** Preparing to stake tokens ***")
    stake_transaction = proxy_contract.functions.stake(stake_amount).build_transaction(
        {
            "chainId": w3.eth.chain_id,
            "gas": 400000,
            "gasPrice": gas_price,
            "nonce": nonce,
        }
    )
    receipt = sign_and_send_transaction(stake_transaction, sender_account)
    receipt_dict = create_receipt_dict(receipt)
    ctx.logger.info(
        f"*** Staking Transaction complete. Receipt details: {receipt_dict} ***"
    )
    await ctx.send(
        sender,
        StakingResponse(
            message="Staking Transaction complete", transaction_receipt=receipt_dict
        ),
    )
 
 
@unstake_agent.on_message(model=StakingRequest, replies=StakingResponse)
async def unstake_handler(ctx: Context, sender: str, msg: StakingRequest):
    sender_account = w3.eth.account.from_key(sender_private_key)
    gas_price = w3.eth.gas_price
    nonce = w3.eth.get_transaction_count(sender_address)
    ctx.logger.info(f"*** Preparing to unstake tokens ***")
    unstake_transaction = proxy_contract.functions.unstake(
        stake_amount
    ).build_transaction(
        {
            "chainId": w3.eth.chain_id,
            "gas": 400000,
            "gasPrice": gas_price,
            "nonce": nonce,
        }
    )
    receipt = sign_and_send_transaction(unstake_transaction, sender_account)
    receipt_dict = create_receipt_dict(receipt)
    ctx.logger.info(
        f"*** Unstaking Transaction complete. Receipt details: {receipt_dict} ***"
    )
    await ctx.send(
        sender,
        StakingResponse(
            message="Unstaking Transaction complete", transaction_receipt=receipt_dict
        ),
    )
 
 
bureau = Bureau()
bureau.add(user_agent)
bureau.add(stake_agent)
bureau.add(unstake_agent)
if __name__ == "__main__":
    bureau.run()
