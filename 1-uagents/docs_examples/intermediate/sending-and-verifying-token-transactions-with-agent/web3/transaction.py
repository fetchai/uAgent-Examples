import json
import os
from typing import Dict, Optional

from dotenv import load_dotenv
from uagents import Agent, Bureau, Context, Model
from web3 import Web3

load_dotenv()
provider_url = os.getenv("WEB3_PROVIDER_URL")
sender_address = os.getenv("SENDER_ADDRESS")
receiver_address = os.getenv("RECEIVER_ADDRESS")
sender_private_key = os.getenv("SENDER_PRIVATE_KEY")
usdc_contract_address = os.getenv("USDC_CONTRACT_ADDRESS")
amount = os.getenv("AMOUNT")


class TransactionRequest(Model):
    message: str
    action: str
    transaction_hash: Optional[str] = None


class TransactionResponse(Model):
    message: str
    balance: Optional[int] = 0
    transaction_receipt: Optional[Dict] = None


class VerificationRequest(Model):
    transaction_hash: str


class VerificationResponse(Model):
    status: str
    receipt: Optional[Dict] = None


with open("abi.json") as abi_file:
    proxy_abi = json.load(abi_file)

w3 = Web3(Web3.HTTPProvider(provider_url))
proxy_contract = w3.eth.contract(address=usdc_contract_address, abi=proxy_abi)


transaction_initiator = Agent(
    name="transaction_initiator", seed="transaction_initiator recovery phrase"
)

transaction_processor = Agent(
    name="transaction_processor", seed="transaction_processor recovery phrase"
)

verification_agent = Agent(
    name="verification_agent", seed="verification_agent recovery phrase"
)


@transaction_initiator.on_event("startup")
async def initiate_transaction(ctx: Context):
    """
    Triggered on startup. Sends a transaction request to the
    transaction processor to initiate a USDC transfer.
    """
    ctx.logger.info("*** Transaction Initiator startup event triggered. ***")
    await ctx.send(
        transaction_processor.address,
        TransactionRequest(message="Requesting transaction", action="send_usdc"),
    )


@transaction_initiator.on_message(
    model=TransactionResponse, replies=VerificationRequest
)
async def transaction_initiator_response_handler(
    ctx: Context, sender: str, msg: TransactionResponse
):
    """
    Handles the transaction response. Logs the transaction
    receipt and sends a verification request if successful.
    """
    ctx.logger.info(f"*** Received response from {sender}: {msg.message} ***")
    if msg.transaction_receipt is not None:
        ctx.logger.info(
            f"*** USDC Transaction successful: {msg.transaction_receipt} ***"
        )
        transaction_hash = msg.transaction_receipt["transactionHash"]
        print(transaction_hash)
        await ctx.send(
            verification_agent.address,
            VerificationRequest(transaction_hash=transaction_hash),
        )


@transaction_processor.on_message(model=TransactionRequest, replies=TransactionResponse)
async def transaction_processor_request_handler(
    ctx: Context, sender: str, msg: TransactionRequest
):
    """
    Processes the transaction request. Builds, signs, and sends a
    USDC transfer transaction, then sends the receipt back.
    """
    ctx.logger.info(
        f"*** Transaction Processor received request from {sender}: {msg.message} with action {msg.action} ***"
    )

    if msg.action == "send_usdc":
        ctx.logger.info(
            f"*** Preparing to send USDC from {sender_address} to {receiver_address} ***"
        )
        sender_account = w3.eth.account.from_key(sender_private_key)
        gas_price = w3.eth.gas_price
        usdc_amount = w3.to_wei(amount, "mwei")
        transaction = proxy_contract.functions.transfer(
            receiver_address, usdc_amount
        ).build_transaction(
            {
                "chainId": w3.eth.chain_id,
                "nonce": w3.eth.get_transaction_count(sender_address),
                "gas": 600000,
                "gasPrice": gas_price,
            }
        )

        signed_txn = sender_account.sign_transaction(transaction)
        raw_transaction = signed_txn.raw_transaction
        tx_hash = w3.eth.send_raw_transaction(raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        receipt_dict = {
            "transactionHash": receipt.transactionHash.hex(),
            "transactionIndex": receipt.transactionIndex,
            "blockNumber": receipt.blockNumber,
            "blockHash": receipt.blockHash.hex(),
            "cumulativeGasUsed": receipt.cumulativeGasUsed,
            "gasUsed": receipt.gasUsed,
            "status": receipt.status,
        }

        ctx.logger.info(
            f"*** USDC Transaction complete. Receipt details: {receipt_dict} ***"
        )

        await ctx.send(
            sender,
            TransactionResponse(
                message="USDC Transaction complete", transaction_receipt=receipt_dict
            ),
        )


@verification_agent.on_message(model=VerificationRequest, replies=VerificationResponse)
async def verification_request_handler(
    ctx: Context, sender: str, msg: VerificationRequest
):
    """
    Verifies the transaction using the provided hash. Logs the
    status and stores the receipt in the agent's context.
    """
    ctx.logger.info(
        f"*** Verification Agent received request: {msg.transaction_hash} ***"
    )

    try:
        receipt = w3.eth.get_transaction_receipt(msg.transaction_hash)
        if receipt:
            status = "Success" if receipt.status == 1 else "Failure"
            receipt_dict = {
                "transactionHash": receipt.transactionHash.hex(),
                "transactionIndex": receipt.transactionIndex,
                "blockNumber": receipt.blockNumber,
                "blockHash": receipt.blockHash.hex(),
                "cumulativeGasUsed": receipt.cumulativeGasUsed,
                "gasUsed": receipt.gasUsed,
                "status": status,
            }
            ctx.logger.info(f"*** Transaction Verification: {status} ***")
            ctx.storage.set("receipt", receipt_dict)
        else:
            ctx.logger.info(f"*** Transaction not found: {msg.transaction_hash} ***")
    except Exception as e:
        ctx.logger.error(f"*** Error during verification: {e} ***")


bureau = Bureau()
bureau.add(transaction_initiator)
bureau.add(transaction_processor)
bureau.add(verification_agent)

if __name__ == "__main__":
    bureau.run()
