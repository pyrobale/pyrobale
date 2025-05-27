from ..pyrobale.client import Client
from ..pyrobale.objects import Message, UpdatesTypes

client = Client("YOUR_BOT_TOKEN")

async def message_handler(message: Message):
    await message.reply("Hello, world!")

client.add_handler(UpdatesTypes.MESSAGE, message_handler)

client.run()