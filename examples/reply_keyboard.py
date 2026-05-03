from pyrobale.client import Client
from pyrobale.objects import Message
from pyrobale.objects import ReplyKeyboardMarkup

client = Client("YOUR_BOT_TOKEN")

@client.on_message()
async def message_handler(message: Message):
    buttons = ReplyKeyboardMarkup()
    buttons.add_button("Hello")
    await message.reply("These are Reply Buttons!", reply_markup=buttons)

client.run()