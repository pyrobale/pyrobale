![pyrobaletext](https://raw.githubusercontent.com/pyrobale/pyrobale/refs/heads/main/pyrobaletext.png)

# Bale Bot API Python Library

A Python wrapper for the Bale Bot API that makes it easy to build Bale bots.

## Features

- Full Bale Bot API support
- Object-oriented design
- Easy-to-use interface
- Support for:
  - Messages
  - Photos
  - Documents
  - Audio
  - Video
  - Voice messages
  - Location
  - Contact sharing
  - Inline keyboards
  - Menu keyboards
  - Callback queries
  - Chat administration
  - Payment system
  - Database integration

## Installation


pip install git+https://github.com/yourusername/bale-bot-python.git


## Quick Start


from bale import Client, MenuKeyboardMarkup, MenuKeyboardButton

# Initialize bot with token
bot = Client("YOUR_BOT_TOKEN")

# Handle incoming messages
@bot.on_message
def handle_message(message):
    if message.text == "/start":
        # Create keyboard
        keyboard = MenuKeyboardMarkup()
        keyboard.add(MenuKeyboardButton("Hello!"))
        
        # Send welcome message
        message.reply_message("Welcome!", reply_markup=keyboard)

# Start the bot
bot.run()


## Key Components

### Client
The main class for interacting with Bale API. Handles all API requests and provides event decorators.

### Message
Represents a message in Bale with methods for replying, editing, and deleting messages.

### User
Represents a Bale user with their properties and methods.

### Chat
Represents a chat conversation with methods for sending messages and managing chat settings.

### Keyboards
- `MenuKeyboardMarkup`: For creating text keyboards
- `InlineKeyboardMarkup`: For creating inline keyboards

### Database
Built-in SQLite database support for storing persistent data.

## Event Handlers


# Message handler
@bot.on_message
def handle_message(message):
    pass

# Callback query handler
@bot.on_callback_query
def handle_callback(callback):
    pass

# Periodic task handler
@bot.on_tick(60)  # Runs every 60 seconds
def handle_tick():
    pass

# Ready event handler
@bot.on_ready
def handle_ready():
    pass

# Member join handler
@bot.on_member_chat_join
def handle_join(message, chat, user):
    pass

# Member leave handler
@bot.on_member_chat_leave
def handle_leave(message, chat, user):
    pass


## Database Usage


# Access database
with bot.database as db:
    # Store data
    db.write_key("user_123", {"points": 100})
    
    # Read data
    data = db.read_key("user_123")


## Running Multiple Bots


from bale import run_multiple_clients

bot1 = Client("TOKEN1")
bot2 = Client("TOKEN2")

run_multiple_clients(bot1, bot2)


## License

This project is licensed under the MIT License - see the LICENSE file for details.
