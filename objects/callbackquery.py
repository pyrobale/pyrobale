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
from ..objects.invoice import (Invoice)
from ..objects.client import (Client)
from ..objects.chatmember import (ChatMember)

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