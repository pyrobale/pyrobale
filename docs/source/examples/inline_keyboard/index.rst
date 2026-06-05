🎯 Inline keyboard
===========

how to create inline keyboard in pyrobale

.. toctree::
   :maxdepth: 2
   :caption: Command example

.. code-block:: python

    from pyrobale.client import Client
    from pyrobale.objects import Message, CallbackQuery
    from pyrobale.objects import InlineKeyboardMarkup
    from pyrobale.objects.enums import ButtonTypes

    client = Client("YOUR_BOT_TOKEN")

    @client.on_message()
    async def message_handler(message: Message):
        buttons = pishnahad_inline = InlineKeyboardMarkup(
      [("Link Button 🚀", "https://google.com", ButtonTypes.URL), ("Web App",https://google.com", ButtonTypes.WEB_APP)],
      [("Callback", "callback_data"), ("Copy TEXT", "This Text Copied", ButtonTypes.COPY_TEXT_BUTTON)])

    @client.on_callback_query()
    async def callback_handler(callback_query: CallbackQuery):
        await callback_query.answer("Callback Query Received!", show_alert=True)

    client.run()
