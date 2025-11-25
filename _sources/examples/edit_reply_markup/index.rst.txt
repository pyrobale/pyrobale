🎯 Edit Inline buttons
===========

how to edit buttons after sending messages.

.. toctree::
   :maxdepth: 2
   :caption: Echo bot example

.. code-block:: python

    import asyncio
    import pyrobale


    bot = pyrobale.Client("YOUR_BOT_TOKEN")

    @bot.on_command("start")
    async def start(message: pyrobale.Message):

        s = await message.reply("Buttons will add in 3 seconds")

        await asyncio.sleep(3)

        btn = pyrobale.InlineKeyboardMarkup()
        btn.add_button("daradege website", url="https://daradege.ir")

        await s.edit_reply_markup(btn)

    bot.run()