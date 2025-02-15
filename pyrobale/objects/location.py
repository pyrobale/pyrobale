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
from pyrobale.objects.contact import (Contact)
from pyrobale.objects.database import (DataBase)
from pyrobale.objects.inputfile import(InputFile)
from pyrobale.objects.labeledprice import (LabeledPrice)
from pyrobale.objects.invoice import (Invoice)
from pyrobale.objects.client import (Client)
from pyrobale.objects.chatmember import (ChatMember)

class Location:
    def __init__(self, data: dict):
        if data:
            self.long = self.longitude = data.get('longitude')
            self.lat = self.latitude = data.get('latitude')
        else:
            self.longitude = self.long = None
            self.latitude = self.lat = None