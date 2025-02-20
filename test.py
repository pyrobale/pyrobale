from pyrobale import *

bot = Client('1925697489:CwP34Ac3liEowK8sDa8hnelH5k5xhT2ezawwmGFo')


@bot.on_message
def handler(message: Message):
    ...

bot.run()