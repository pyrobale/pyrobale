from pyrobale.client import Client


bot = Client("1506646393:Nbw9GaJ_ZV6SCIeMuP7wdw0SedJHVVV4Th4")


@bot.on_message()
async def test(message):
    testi = await bot.get_chat_member(5430437322, 348813968)
    print(testi.inputs)

bot.run()