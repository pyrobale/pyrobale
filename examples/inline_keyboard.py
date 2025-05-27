from pyrobale.client import Client
from pyrobale.objects import Message, UpdatesTypes, CallbackQuery
from pyrobale.objects import InlineKeyboardButton, InlineKeyboardMarkup, CopyTextButton

client = Client("YOUR_BOT_TOKEN")

@client.on_message()
async def message_handler(message: Message):
    buttons = InlineKeyboardMarkup()
    buttons.add_button("Callback", callback_data="callback_data")
    buttons.add_button("Copy Text", copy_text=CopyTextButton("Hello, world!"))
    buttons.add_button("URL", url="https://www.google.com")
    buttons.add_button("WebApp", web_app="https://daradege.ir")
    await message.reply("These are Inline Buttons!", reply_markup=buttons)

@client.on_callback_query()
async def callback_handler(callback_query: CallbackQuery):
    await callback_query.answer("Callback Query Received!", show_alert=True)

client.run()