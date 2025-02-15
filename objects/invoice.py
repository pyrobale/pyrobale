import json
import time
from typing import Optional, Dict, Any, List, Union
import threading
import traceback
import sqlite3
import inspect
import requests
from ..exceptions.base import (BaleException)
from ..objects.keyboards import (InlineKeyboardButton,InlineKeyboardMarkup,MenuKeyboardButton,MenuKeyboardMarkup)
from ..objects.callbackquery import (CallbackQuery)
from ..objects.chat import (Chat)
from ..objects.voice import (Voice)
from ..objects.document import (Document)
from ..objects.photo import (Photo)
from ..objects.message import (Message)
from ..objects.user import (User)
from ..objects.location import (Location)
from ..objects.contact import (Contact)
from ..objects.database import (DataBase)
from ..objects.inputfile import(InputFile)
from ..objects.labeledprice import (LabeledPrice)
from ..objects.client import (Client)
from ..objects.chatmember import (ChatMember)

class Invoice:
    def __init__(self, data: dict):
        if data:
            self.title = data.get('title')
            self.description = data.get('description')
            self.start_parameter = data.get('start_parameter')
            self.currency = data.get('currency')
            self.total_amount = data.get('total_amount')
        else:
            self.title = None
            self.description = None
            self.start_parameter = None
            self.currency = None
            self.total_amount = None