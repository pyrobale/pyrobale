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
from pyrobale.objects.invoice import (Invoice)
from pyrobale.objects.client import (Client)

class ChatMember:
    def __init__(self, client: 'Client', data: Dict[str, Any]):
        if data:
            self.status = data.get('status')
            self.user = User(
                client, {
                    'ok': True, 'result': data.get(
                        'user', {})})
            self.is_anonymous = data.get('is_anonymous')
            self.can_be_edited = data.get('can_be_edited')
            self.can_manage_chat = data.get('can_manage_chat')
            self.can_delete_messages = data.get('can_delete_messages')
            self.can_manage_video_chats = data.get('can_manage_video_chats')
            self.can_restrict_members = data.get('can_restrict_members')
            self.can_promote_members = data.get('can_promote_members')
            self.can_change_info = data.get('can_change_info')
            self.can_invite_users = data.get('can_invite_users')
            self.can_pin_messages = data.get('can_pin_messages')
            self.can_manage_topics = data.get('can_manage_topics')
            self.is_creator = data.get('status') == 'creator'