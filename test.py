import pyrobale

TOKEN, ADMIN = "1744668654:AV24LrBA7Hehq816gQEJs2dB6QSIsI2Gg1FP5v3F", [1386783796]
gok = ADMIN[0]
bot = pyrobale.Client(TOKEN)

@bot.on_command("/start")
def start(message: pyrobale.Message):
    btn = pyrobale.InlineKeyboardMarkup()
    btn.add(pyrobale.InlineKeyboardButton("ارسال پیام به استانداری شمیرانات", "sendmessage"), 2)
    btn.add(pyrobale.InlineKeyboardButton("درباره ما", "about"), 3)
    message.reply("""
سلام!🖐️ 
به ربات استانداری شمیرانات خوش آمدید!🤩
برای استفاده از ابزار های ربات، روی دمه های زیر کلیک کنید:""", reply_markup=btn)

@bot.on_message
def sendMsg(message: pyrobale.Message):
        
    if message.author.get_state() == "sendMsg":
        try:
            bot.send_message(ADMIN[0], f"{message.chat.id}-{message.id}-\n"+message.text)
            message.reply("پیام شما با موفقیت ارسال شد!")
            message.author.set_state(None)
        except Exception as e:
            message.reply("خطا در ارسال پیام")
            print(e)

    if message.chat.id == gok and message.reply_to_message:
        if 1:
            message_chat = message.reply_to_message.text.split('-')[0]
            message_id = message.reply_to_message.text.split('-')[1]
            
            print(message_chat, message_id)
            
            if message.text and message.author.id in ADMIN:
                bot.send_message(
                    message_chat,
                    message.text.removeprefix(f"{message_chat}-{message_id}-"),
                    reply_to_message=str(message_id)
                )


@bot.on_callback_query
def callback(callback_query):
    try:
        if callback_query.data == "sendmessage":
            callback_query.message.reply("لطفا پیام خود را ارسال کنید:")
            callback_query.author.set_state("sendMsg")
        elif callback_query.data == "about":
            callback_query.message.reply("استانداری شمیرانات فعالیت خود را به طور مخفی از زمان تشکیل جهان هستی آغاز کرده است و هنوز هم به طور کاملا *مخفی* فعالیت دارد، به طوری که هیچکس تا کنون این استاندار مرموز را ندیده است...")
    except Exception as e:
        print(e)

bot.run()