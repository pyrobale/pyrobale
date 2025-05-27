from pyrobale.client import Client
from pyrobale.objects import Message, UpdatesTypes

client = Client("YOUR_BOT_TOKEN")

@client.on_message()
async def message_handler(message: Message):
    await message.reply(message.text)

client.run()