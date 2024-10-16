from cosmpy.aerial.wallet import LocalWallet
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.crypto.keypairs import PrivateKey
from uagents import Agent, Context, Model
from uagents.network import get_faucet, wait_for_tx_to_complete

mainnet_ledger = LedgerClient(NetworkConfig.fetchai_mainnet())


class RequestWithTX(Model):
    message: str
    tx_hash: str


class DataResponse(Model):
    message: str


class PaymentError(Model):
    message: str
    tx_hash: str


DataSellingAgent = Agent(
    name="DataSellingAgent",
    seed="dwefwegferdwdwedgko4o430490349jf340-jffjweiopfnw",
    port=8001,
    endpoint=["http://localhost:8001/submit"],
)

print(DataSellingAgent.address)

AMOUNT = 1
DENOM = "afet"
DATA_TO_SELL = "..."

## at first you may want to generate a wallet
my_wallet = LocalWallet.generate()
## or open one from a seed you've set
# my_wallet = LocalWallet.from_unsafe_seed("registration test wallet")
# pk = my_wallet._private_key
## or from a pk you already have
# wallet = LocalWallet(PrivateKey("T7w1yHq1QIcQiSqV27YSwk+i1i+Y4JMKhkpawCQIh6s="))

...


@DataSellingAgent.on_message(model=RequestWithTX)
async def message_handler(ctx: Context, sender: str, msg: RequestWithTX):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

    mainnet_ledger.query_tx(msg.tx_hash)
    tx_resp = await wait_for_tx_to_complete(msg.tx_hash, mainnet_ledger)

    coin_received = tx_resp.events["coin_received"]
    if (
            coin_received["receiver"] == str(my_wallet.address)
            and coin_received["amount"] == f"{AMOUNT}{DENOM}"
    ):
        ctx.logger.info(f"Transaction was successful: {coin_received}")
        await ctx.send(sender, DataResponse(message=DATA_TO_SELL))

    else:
        await ctx.send(sender, PaymentError(message="Incorrect tx", tx_hash=msg.tx_hash))


if __name__ == "__main__":
    DataSellingAgent.run()