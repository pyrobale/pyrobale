🎯 Command
===========

how to add command to pyrobale

.. toctree::
   :maxdepth: 2
   :caption: Command example


.. code-block:: python

    from pyrobale import Client, Message

    token = "YOUR_BOT_TOKEN"

    bot = Client(token)

    @bot.on_command('start')
    async def start(message: Message):
        await message.reply("Hello, world!")

    bot.run()