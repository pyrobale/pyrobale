from pyrobale import Client, Message

bot = Client("YOUR_BOT_TOKEN")

bot.defined_messages = {
    "/start": "Hello! welcome to Pyrobale!",
    "/help": "I cannot help you now :)"
}

bot.check_defined_message = True

bot.run()