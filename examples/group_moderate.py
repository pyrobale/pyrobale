from pyrobale import Client, Message

client = Client("YOUR_BOT_TOKEN")

@client.on_command("mute")
async def mute_chat_member(message: Message):
    chat_member = await message.chat.get_chat_member(message.user.id)
    await chat_member.mute()

@client.on_command("unmute")
async def unmute_chat_member(message: Message):
    chat_member = await message.chat.get_chat_member(message.user.id)
    await chat_member.unmute()

@client.on_command("ban")
async def ban_chat_member(message: Message):
    chat_member = await message.chat.get_chat_member(message.user.id)
    await chat_member.ban()

@client.on_command("unban")
async def unban_chat_member(message: Message):
    chat_member = await message.chat.get_chat_member(message.user.id)
    await chat_member.unban()

@client.on_command("kick")
async def kick_chat_member(message: Message):
    chat_member = await message.chat.get_chat_member(message.user.id)
    await chat_member.kick()

client.run()