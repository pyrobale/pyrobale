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
from ..objects.database import (DataBase)
from ..objects.inputfile import(InputFile)
from ..objects.labeledprice import (LabeledPrice)
from ..objects.invoice import (Invoice)
from ..objects.client import (Client)
from ..objects.chatmember import (ChatMember)

class Contact:
    def __init__(self, data: dict):
        if data:
            self.phone_number = data.get('phone_number')
            self.first_name = data.get('first_name')
            self.last_name = data.get('last_name')
            self.user_id = data.get('user_id')
        else:
            self.phone_number = None
            self.first_name = None
            self.last_name = None
            self.user_id = None