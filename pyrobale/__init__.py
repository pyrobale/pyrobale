"""
![pyrobaletext](https://raw.githubusercontent.com/pyrobale/pyrobale/refs/heads/main/pyrobaletext.png)

# Bale Bot API Python Library

A modern, easy-to-use Python wrapper for the Bale Bot API that makes building Bale bots simple and intuitive.

## Features

- 🚀 **Simple & Intuitive** - Clean, Pythonic API design
- 📨 **Full Message Support** - Text, photos, videos, documents, and more
- ⌨️ **Interactive Elements** - Inline keyboards, reply keyboards, and buttons
- 🔄 **Real-time Updates** - Webhook and polling support
- 📁 **File Handling** - Easy upload and download of media files
- 🛡️ **Error Handling** - Comprehensive exception handling
- 📖 **Type Hints** - Full typing support for better development experience
- ⚡ **Async Support** - Both synchronous and asynchronous operations

## Installation

```bash
pip install pyrobale
```

## Quick Start

```python
from pyrobale.client import Client
from pyrobale.objects import Message, UpdatesTypes

bot = Client("YOUR_BOT_TOKEN")

@bot.on_message()
async def message_handler(message: Message):
    await message.reply("Hello, world!")

bot.run()
```

## Examples

### Conversation Bot
```python
from pyrobale.objects import *
from pyrobale.client import Client, Message, UpdatesTypes
import asyncio

client = Client("YOUR_BOT_TOKEN")

async def handle_message(message: Message):
    if message.text == "/start":
        await message.reply("سلام! من یک ربات PyRoBale هستم!")
        await client.wait_for(UpdatesTypes.MESSAGE)
        await message.reply("Okay! wait_for Test Compeleted")

client.add_handler(UpdatesTypes.MESSAGE, handle_message)

client.run()
```

### Echo Bot
```python
from pyrobale.client import Client
from pyrobale.objects import Message, UpdatesTypes

bot = Client("YOUR_BOT_TOKEN")

@bot.on_message()
async def message_handler(message: Message):
    await message.reply(message.text)

bot.run()
```

### Inline Keyboard
```python
from pyrobale.client import Client
from pyrobale.objects import Message, UpdatesTypes, InlineKeyboardButton, InlineKeyboardMarkup, CopyTextButton

bot = Client("YOUR_BOT_TOKEN")
async def message_handler(message: Message):
    buttons = InlineKeyboardMarkup()
    buttons.add_button("URL", url="https://google.com")
    buttons.add_button("Callback", callback_data="callback")
    buttons.add_row()
    buttons.add_button("WebApp", web_app="https://daradege.ir")
    buttons.add_button("Copy", copy_text_button=CopyTextButton("TEXT"))
    await message.reply("Hello, world!", reply_markup=buttons)
```


## Core Abilities

- **Message Handling** - Process text, commands, and media messages
- **Callback Queries** - Handle inline keyboard interactions
- **File Operations** - Send and receive photos, videos, documents
- **Chat Management** - Get chat info, member management
- **Custom Keyboards** - Create interactive user interfaces
- **Webhook Support** - Production-ready webhook handling
- **Middleware Support** - Add custom processing layers

## Documentation

For detailed documentation and advanced usage, visit our [documentation site](https://pyrobale.readthedocs.io).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📖 [Documentation](https://pyrobale.readthedocs.io)
- 🐛 [Issue Tracker](https://github.com/pyrobale/pyrobale/issues)
- 💬 [Discussions](https://github.com/pyrobale/pyrobale/discussions)

"""

from .objects.utils import *
from .exceptions import *
from .objects import *
from .client import Client
