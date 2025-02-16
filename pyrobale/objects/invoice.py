import json
import time
from typing import Optional, Dict, Any, List, Union
import threading
import traceback
import sqlite3
import inspect
import requests
from pyrobale.exceptions.base import (BaleException)
from pyrobale.objects.keyboards import (InlineKeyboardButton,InlineKeyboardMarkup,MenuKeyboardButton,MenuKeyboardMarkup)
from pyrobale.objects.callbackquery import (CallbackQuery)
from pyrobale.objects.chat import (Chat)
from pyrobale.objects.voice import (Voice)
from pyrobale.objects.document import (Document)
from pyrobale.objects.photo import (Photo)
from pyrobale.objects.message import (Message)
from pyrobale.objects.user import (User)
from pyrobale.objects.location import (Location)
from pyrobale.objects.contact import (Contact)
from pyrobale.objects.database import (DataBase)
from pyrobale.objects.inputfile import(InputFile)
from pyrobale.objects.labeledprice import (LabeledPrice)
from pyrobale.objects.client import (Client)
from pyrobale.objects.chatmember import (ChatMember)

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