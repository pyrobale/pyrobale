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
from ..objects.labeledprice import (LabeledPrice)
from ..objects.invoice import (Invoice)
from ..objects.client import (Client)
from ..objects.chatmember import (ChatMember)

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