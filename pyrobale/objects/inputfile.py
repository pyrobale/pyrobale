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
from pyrobale.objects.labeledprice import (LabeledPrice)
from pyrobale.objects.invoice import (Invoice)
from pyrobale.objects.client import (Client)
from pyrobale.objects.chatmember import (ChatMember)

class InputFile:
    """Represents a file to be uploaded"""

    def __init__(self,
                 client: 'Client',
                 file: Union[str,
                             bytes],
                 filename: Optional[str] = None):
        self.client = client
        self.filename = filename
        if isinstance(file, str):
            if file.startswith(('http://', 'https://')):
                r = requests.get(file)
                r.raise_for_status()
                self.file = r.content
            else:
                try:
                    self.file = open(file, 'rb')
                except IOError:
                    raise BaleException(
                        f"Failed to open file: {traceback.format_exc()}")
        else:
            self.file = file

    def __del__(self):
        if hasattr(self, 'file') and hasattr(self.file, 'close'):
            self.file.close()

    @property
    def to_bytes(self):
        if hasattr(self.file, 'read'):
            return self.file.read()
        return self.file