from pyrobale import Client, Message, UpdatesTypes

bot = Client("YOUR_BOT_TOKEN")

@bot.on_command("/start")
async def start(message: Message):
    await message.reply("what's your name?")
    def check(m: Message):
        return m.user.id == message.user.id
    answer = await bot.wait_for(UpdatesTypes.MESSAGE, check=check)

    await answer.reply(f"Hi {answer.text}!")


bot.run()
