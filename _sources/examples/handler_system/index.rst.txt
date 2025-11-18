🎯 Custom handler
===========

how to add custom handler in pyrobale

.. toctree::
   :maxdepth: 2
   :caption: Command example

.. code-block:: python

    from pyrobale import Client, Message, UpdatesTypes

    client = Client("YOUR_BOT_TOKEN")

    async def message_handler(message: Message):
        await message.reply("Hello, world!")

    client.add_handler(UpdatesTypes.MESSAGE, message_handler)

    client.run()