🎯 Use filters
===========

how to use filters in handlers

.. toctree::
   :maxdepth: 2
   :caption: Echo bot example

.. code-block:: python

    import pyrobale
    from pyrobale.filters import equals, digit, pv


    bot = pyrobale.Client("YOUR_BOT_TOKEN")

    # only if message text was "hi"
    @bot.on_message(equals("hi"))
    async def equals_message(message: pyrobale.Message):
        await message.reply("Hello!")

    # only if text was created from numbers (like "123456")
    @bot.on_message(digit)
    async def digit_message(message: pyrobale.Message):
        await message.reply("Its digit!")

    # only if message was in private chat and text was "hi"
    @bot.on_message(pv, equal("hi"))
    async def pv_equals_message(message: pyrobale.Message):
        await message.reply("Hello in private!")

    # only if callback data was "hi"
    @bot.on_callback_query(equals("cb_987978"))
    async def equals_callback(callback: pyrobale.CallbackQuery):
        await callback.answer("Hello!")


    bot.run()