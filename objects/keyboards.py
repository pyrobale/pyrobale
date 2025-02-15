import json
import time
from typing import Optional, Dict, Any, List, Union
import threading
import traceback
import sqlite3
import inspect
import requests
from ..exceptions.base import (BaleException)
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
from ..objects.invoice import (Invoice)
from ..objects.client import (Client)
from ..objects.chatmember import (ChatMember)

class MenuKeyboardButton:
    def __init__(
            self,
            text: str,
            request_contact: bool = False,
            request_location: bool = False):
        if not text:
            raise ValueError("Text cannot be empty")
        if request_contact and request_location:
            raise ValueError("Cannot request both contact and location")

        self.button = {"text": text}
        if request_contact:
            self.button["request_contact"] = True
        if request_location:
            self.button["request_location"] = True


class InlineKeyboardButton:
    def __init__(
            self,
            text: str,
            callback_data: Optional[str] = None,
            url: Optional[str] = None,
            web_app: Optional[str] = None):
        self.button = {"text": text}
        if sum(bool(x) for x in [callback_data, url, web_app]) != 1:
            raise ValueError(
                "Exactly one of callback_data, url, or web_app must be provided")
        if callback_data:
            self.button["callback_data"] = callback_data
        elif url:
            self.button["url"] = url
        elif web_app:
            self.button["web_app"] = {"url": web_app}


class MenuKeyboardMarkup:
    def __init__(self):
        self.menu_keyboard = []

    def add(self, button: MenuKeyboardButton,
            row: int = 0) -> 'MenuKeyboardMarkup':
        if row < 0:
            raise ValueError("Row index cannot be negative")
        while len(self.menu_keyboard) <= row:
            self.menu_keyboard.append([])
        self.menu_keyboard[row].append(button.button)
        self.cleanup_empty_rows()
        return self

    def cleanup_empty_rows(self) -> None:
        self.menu_keyboard = [row for row in self.menu_keyboard if row]

    def clear(self) -> None:
        self.menu_keyboard = []

    def remove_button(self, text: str) -> bool:
        found = False
        for row in self.menu_keyboard:
            for button in row[:]:
                if button.get('text') == text:
                    row.remove(button)
                    found = True
        self.cleanup_empty_rows()
        return found

    @property
    def keyboard(self):
        return {"keyboard": self.menu_keyboard}


class InlineKeyboardMarkup:
    def __init__(self):
        self.inline_keyboard = []

    def add(self, button: InlineKeyboardButton,
            row: int = 0) -> 'InlineKeyboardMarkup':
        if row < 0:
            raise ValueError("Row index cannot be negative")
        while len(self.inline_keyboard) <= row:
            self.inline_keyboard.append([])
        self.inline_keyboard[row].append(button.button)
        self.cleanup_empty_rows()
        return self

    def cleanup_empty_rows(self) -> None:
        self.inline_keyboard = [row for row in self.inline_keyboard if row]

    def clear(self) -> None:
        self.inline_keyboard = []

    def remove_button(self, text: str) -> bool:
        found = False
        for row in self.inline_keyboard:
            for button in row[:]:
                if button.get('text') == text:
                    row.remove(button)
                    found = True
        self.cleanup_empty_rows()
        return found

    @property
    def keyboard(self) -> dict:
        return {"inline_keyboard": self.inline_keyboard}