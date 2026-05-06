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

List of all filters:

- `equals(excepted_text: str)` 
  - **Usable in Message & CallbackQuery**
  - Checks if message text/caption or callback data is equal with given text

- `startswith(excepted_text: str)`
  - **Usable in Message & CallbackQuery**
  - Checks if message text/caption or callback data is starting with given text

- `regex(pattern: str)`
  - **Usable in Message & CallbackQuery**
  - Checks the event text or caption with given pattern using regex

- `from_users(allowed_users: Union[List[Union["User", int, str]], int, str])`
  - **Usable in All types of events**
  - Check if the event text or caption or callbackQuery sender is in allowed user.

- `is_joined(chat_ids: Union[List[Union["User", int, str]], int, str])`
  - **Usable in All types of events**
  - Check if the event User is joined in specified chats

- `at_state(state: str)`
  - **Usable in All types of events**
  - Check if the event User is at specified state

- `pv`
  - **Usable in All types of events**
  - checks if the event is happening in a private chat

- `group`
  - **Usable in All types of events**
  - checks if the event is happening in a group chat

- `digit`
  - **Usable in All types of events**
  - Check if the event text or caption or callbackQuery data is digit

- `text`
  - **Usable in All types of events**
  - Checks if the event is having text

- `photo`
  - **Usable in All types of events**
  - Checks if the event is having photo

- `video`
  - **Usable in All types of events**
  - Checks if the event is having video

- `audio`
  - **Usable in All types of events**
  - Checks if the event is having audio

- `voice`
  - **Usable in All types of events**
  - Checks if the event is having voice

- `contact`
  - **Usable in All types of events**
  - Checks if the event is having contact

- `location`
  - **Usable in All types of events**
  - Checks if the event is having location
