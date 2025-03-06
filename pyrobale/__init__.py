"""
PyRobale - A Python library for developing bale bots.

Features:
- Simple and fast
- Customizable and Customized
- New and Up to date
- Internal database management
- Easy to use
- Eazy to learn
"""
from typing import Optional, Dict, Any, List, Union

import threading
from .base import Client
from .models import (DataBase,Document,ChatMember,Contact,CallbackQuery,Chat,ChatActions,Voice,User,Photo,Message,MenuKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup,Invoice,InputMediaVideo,InputFile,MenuKeyboardButton,LabeledPrice,InputMediaPhoto,InputMediaAnimation,InputMedia,InputMediaAudio,Location,InputMediaDocument)

__all__ = ['Client','DataBase','Document','ChatMember','Contact','CallbackQuery','Chat','ChatActions','Voice','User','Photo','Message','MenuKeyboardMarkup','InlineKeyboardButton','InlineKeyboardMarkup','Invoice','InputMediaVideo','InputFile','MenuKeyboardButton','LabeledPrice','InputMediaPhoto','InputMediaAnimation','InputMedia','InputMediaAudio','Location','InputMediaDocument']

__version__ = '0.2.9.1'



def run_multiple_bots(bots: List[Client]):
    """Run multiple bots in separate threads"""
    threads = []
    for bot in bots:
        thread = threading.Thread(target=bot.run)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    return bots


def stop_bots(bots: List[Client]):
    """Stop multiple bots gracefully"""
    for bot in bots:
        bot.safe_close()
