from pyrobale import Client, Message

client = Client("YOUR_BOT_TOKEN")

@client.on_message()
async def message_handler(message: Message):
    await message.reply(message.text)

client.run()