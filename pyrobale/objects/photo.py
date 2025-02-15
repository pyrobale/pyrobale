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
from pyrobale.objects.message import (Message)
from pyrobale.objects.user import (User)
from pyrobale.objects.location import (Location)
from pyrobale.objects.contact import (Contact)
from pyrobale.objects.database import (DataBase)
from pyrobale.objects.inputfile import(InputFile)
from pyrobale.objects.labeledprice import (LabeledPrice)
from pyrobale.objects.invoice import (Invoice)
from pyrobale.objects.client import (Client)
from pyrobale.objects.chatmember import (ChatMember)

class Photo:
    def __init__(self, data):
        if data:
            self.file_id = data.get('file_id')
            self.file_unique_id = data.get('file_unique_id')
            self.width = data.get('width')
            self.height = data.get('height')
            self.file_size = data.get('file_size')
        else:
            self.file_id = None
            self.file_unique_id = None
            self.width = None
            self.height = None
            self.file_size = None