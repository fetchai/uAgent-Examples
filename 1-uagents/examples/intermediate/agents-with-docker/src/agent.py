 
from uagents import Agent, Bureau, Context, Model
 
 
class DataPacket(Model):
    message: str
 
 
data_sender = Agent(name="data_sender", seed="data_sender recovery phrase")
data_receiver = Agent(name="data_receiver", seed="data_receiver recovery phrase")
 
 
@data_sender.on_interval(period=4.0)
async def send_data_packet(ctx: Context):
    """
    Event handler that gets triggered at regular intervals (every 4 seconds).
 
    Args:
    ctx (Context): The context in which the event is triggered.
 
    Returns:
    None: This function does not return any value but sends a DataPacket message from data_sender to data_receiver at intervals of (every 4 seconds).
    """
    await ctx.send(
        data_receiver.address, DataPacket(message="Initiating data transfer")
    )
 
 
@data_sender.on_message(model=DataPacket)
async def data_sender_message_handler(ctx: Context, sender: str, msg: DataPacket):
    """
    Event handler that gets triggered when data_sender receives a DataPacket message.
 
    Args:
    ctx (Context): The context in which the event is triggered.
    sender (str): The address of the sender.
    msg (DataPacket): The message received.
 
    Returns:
    None: This function does not return any value but logs the received message.
    """
    ctx.logger.info(f"Data Sender received a message from {sender}: {msg.message}")
 
 
@data_receiver.on_message(model=DataPacket)
async def data_receiver_message_handler(ctx: Context, sender: str, msg: DataPacket):
    """
    Event handler that gets triggered when data_receiver receives a DataPacket message.
 
    Args:
    ctx (Context): The context in which the event is triggered.
    sender (str): The address of the sender.
    msg (DataPacket): The message received.
 
    Returns:
    None: This function does not return any value but logs the received message and sends an acknowledgment back to data_sender.
    """
    ctx.logger.info(f"Data Receiver received a message from {sender}: {msg.message}")
    await ctx.send(
        data_sender.address, DataPacket(message="Acknowledging data transfer")
    )
 
 
bureau = Bureau()
bureau.add(data_sender)
bureau.add(data_receiver)
 
if __name__ == "__main__":
    bureau.run()