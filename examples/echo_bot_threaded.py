from pyrobale import Client, Message

client = Client("YOUR_BOT_TOKEN")

@client.on_message()
def message_handler(message: Message):
    message.reply(message.text)

client.run()