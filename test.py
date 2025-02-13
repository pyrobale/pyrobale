import pyrobale

client = pyrobale.Client("1925697489:CwP34Ac3liEowK8sDa8hnelH5k5xhT2ezawwmGFo")

@client.on_message
def handler(message:pyrobale.Message):
    message.reply_message("Hello, world!")

@client.on_ready
def ready_handler():
    print("Bot is ready!")

client2 = pyrobale.Client(client.token)

@client2.on_message
def handledr(message:pyrobale.Message):
    message.reply_message("Hello, wordld!")