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
from pyrobale.objects.invoice import (Invoice)
from pyrobale.objects.client import (Client)
from pyrobale.objects.chatmember import (ChatMember)

class CallbackQuery:
    """Represents a callback query from a callback button"""

    def __init__(self, client: 'Client', data: Dict[str, Any]):
        if not data.get('ok'):
            raise BaleException(
                f"API request failed: {traceback.format_exc()}")
        self.client = client
        result = data.get('result', {})
        self.id = result.get('id')
        self.from_user = self.user = self.author = User(
            client, {'ok': True, 'result': result.get('from', {})})
        self.message = Message(
            client, {
                'ok': True, 'result': result.get(
                    'message', {})})
        self.inline_message_id = result.get('inline_message_id')
        self.chat_instance = result.get('chat_instance')
        self.data = result.get('data')

    def answer(self,
               text: str,
               reply_markup: Optional[Union[MenuKeyboardMarkup,
                                            InlineKeyboardMarkup]] = None) -> 'Message':
        return self.client.send_message(
            chat_id=self.message.chat.id,
            text=text,
            reply_markup=reply_markup)

    def reply(self,
              text: str,
              reply_markup: Optional[Union[MenuKeyboardMarkup,
                                           InlineKeyboardMarkup]] = None) -> 'Message':
        return self.client.send_message(
            chat_id=self.message.chat.id,
            text=text,
            reply_markup=reply_markup,
            reply_to_message=self.message.id)