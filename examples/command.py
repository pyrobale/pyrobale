from pyrobale.client import Client
from pyrobale.objects import Message, UpdatesTypes

token = "YOUR_BOT_TOKEN"

bot = Client(token)

@bot.on_command('start')
async def start(message: Message):
    await message.reply("Hello, world!")

bot.run()