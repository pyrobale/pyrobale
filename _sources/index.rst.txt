Pyrobale Documentation
=====================

A new python library designed to be modern, fast and useful.

.. toctree::
   :maxdepth: 2
   :caption: API Documents

   api/index

Examples
--------------

install stable release:

.. code-block:: bash

   pip install pyrobale


Simple use:

.. code-block:: python

   import pyrobale

   bot = pyrobale.Client("YOUR_BOT_TOKEN")

   @bot.on_command("start")
   async def command(message: pyrobale.Message):
       await message.reply("Hello!")

   bot.run()

Index & tables
===============

* :ref:`genindex`
* :ref:`modindex` 
* :ref:`search`