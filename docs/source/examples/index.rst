🎯 Examples
===========

Examples of using Pyrobale

.. toctree::
   :maxdepth: 2
   :caption: Examples

   echo-bot
   command-handler
   inline-keyboard
   state-machine

Quick start
----------

.. code-block:: python

   from pyrobale import Client
   from pyrobale.filters import text_filter

   bot = Client("YOUR_BOT_TOKEN")

   @bot.on_message(text_filter("hi"))
   async def hello_handler(client, message):
       await message.reply("hi! 👋")

   bot.run()