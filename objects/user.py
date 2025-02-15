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
from ..objects.location import (Location)
from ..objects.contact import (Contact)
from ..objects.database import (DataBase)
from ..objects.inputfile import(InputFile)
from ..objects.labeledprice import (LabeledPrice)
from ..objects.invoice import (Invoice)
from ..objects.client import (Client)
from ..objects.chatmember import (ChatMember)

class User:
    """Represents a Bale user"""

    def __init__(self, client: 'Client', data: Dict[str, Any]):
        if not data.get('ok'):
            raise BaleException(
                f"API request failed: {traceback.format_exc()}")
        self.client = client
        result = data.get('result', {})
        self.data = data
        self.ok = data.get('ok')
        self.id = result.get('id')
        self.is_bot = result.get('is_bot')
        self.first_name = result.get('first_name')
        self.last_name = result.get('last_name')
        self.username = result.get('username')

    def set_state(self, state: str) -> None:
        """Set the state for a chat or user"""
        self.client.states[str(self.id)] = state

    def get_state(self) -> str | None:
        """Get the state for a chat or user"""
        return self.client.states.get(str(self.id))

    def del_state(self) -> None:
        """Delete the state for a chat or user"""
        self.client.states.pop(str(self.id), None)

    def send_message(self,
                     text: str,
                     parse_mode: Optional[str] = None,
                     reply_markup: Union[MenuKeyboardMarkup,
                                         InlineKeyboardMarkup] = None) -> 'Message':
        """Send a message to this user"""
        return self.client.send_message(
            self.id, text, parse_mode, reply_markup)

    def send_photo(self,
                   photo: Union[str,
                                bytes,
                                InputFile],
                   caption: Optional[str] = None,
                   parse_mode: Optional[str] = None,
                   reply_markup: Union[MenuKeyboardMarkup,
                                       InlineKeyboardMarkup] = None) -> 'Message':
        """Send a photo to a chat"""
        return self.client.send_photo(
            self.id, photo, caption, parse_mode, reply_markup)

    def forward_message(
            self, from_chat_id: Union[int, str], message_id: int) -> 'Message':
        """Forward a message to this user"""
        self.client.forward_message(self.id, from_chat_id, message_id)

    def copy_message(self,
                     from_chat_id: Union[int,
                                         str],
                     message_id: int) -> 'Message':
        """Copy a message to this user"""
        self.client.copy_message(self.id, from_chat_id, message_id)

    def send_audio(self,
                   audio: Union[str,
                                bytes,
                                InputFile],
                   caption: Optional[str] = None,
                   parse_mode: Optional[str] = None,
                   reply_markup: Union[MenuKeyboardMarkup,
                                       InlineKeyboardMarkup] = None,
                   reply_to_message: Union[str,
                                           int,
                                           'Message'] = None) -> 'Message':
        """Send an audio file to this user"""
        self.client.send_audio(
            self.id,
            audio,
            caption,
            parse_mode,
            reply_markup,
            reply_to_message)

    def send_document(self,
                      document: Union[str,
                                      bytes,
                                      InputFile],
                      caption: Optional[str] = None,
                      parse_mode: Optional[str] = None,
                      reply_markup: Union[MenuKeyboardMarkup,
                                          InlineKeyboardMarkup] = None,
                      reply_to_message: Union[str,
                                              int,
                                              'Message'] = None) -> 'Message':
        """Send a document to this user"""
        self.client.send_document(
            self.id,
            document,
            caption,
            parse_mode,
            reply_markup,
            reply_markup)

    def send_video(self,
                   video: Union[str,
                                bytes,
                                InputFile],
                   caption: Optional[str] = None,
                   parse_mode: Optional[str] = None,
                   reply_markup: Union[MenuKeyboardMarkup,
                                       InlineKeyboardMarkup] = None,
                   reply_to_message: Union[str,
                                           int,
                                           'Message'] = None) -> 'Message':
        """Send a video to this user"""
        self.client.send_video(
            self.id,
            video,
            caption,
            parse_mode,
            reply_markup,
            reply_to_message)

    def send_animation(self,
                       animation: Union[str,
                                        bytes,
                                        InputFile],
                       caption: Optional[str] = None,
                       parse_mode: Optional[str] = None,
                       reply_markup: Union[MenuKeyboardMarkup,
                                           InlineKeyboardMarkup] = None,
                       reply_to_message: Union[int,
                                               str,
                                               'Message'] = None) -> 'Message':
        """Send an animation to this user"""
        return self.client.send_animation(
            self.id,
            animation,
            caption,
            parse_mode,
            reply_markup,
            reply_to_message)

    def send_voice(self,
                   voice: Union[str,
                                bytes,
                                InputFile],
                   caption: Optional[str] = None,
                   parse_mode: Optional[str] = None,
                   reply_markup: Union[MenuKeyboardMarkup,
                                       InlineKeyboardMarkup] = None,
                   reply_to_message: Union[int,
                                           str,
                                           'Message'] = None) -> 'Message':
        """Send a voice message to this user"""
        return self.client.send_voice(
            self.id,
            voice,
            caption,
            parse_mode,
            reply_markup,
            reply_to_message)

    def send_media_group(self,
                         chat_id: Union[int,
                                        str],
                         media: List[Dict],
                         reply_to_message: Union['Message',
                                                 int,
                                                 str] = None) -> List['Message']:
        """Send a group of photos, videos, documents or audios as an album"""
        return self.client.send_media_group(chat_id, media, reply_to_message)

    def send_location(self,
                      latitude: float,
                      longitude: float,
                      reply_markup: Union[MenuKeyboardMarkup,
                                          InlineKeyboardMarkup] = None,
                      reply_to_message: Union[str,
                                              int,
                                              'Message'] = None) -> 'Message':
        """Send a location to this user"""
        return self.send_location(
            latitude,
            longitude,
            reply_markup,
            reply_to_message)

    def send_contact(self,
                     phone_number: str,
                     first_name: str,
                     last_name: Optional[str] = None,
                     reply_markup: Union[MenuKeyboardMarkup,
                                         InlineKeyboardMarkup] = None,
                     reply_to_message: Union[str,
                                             int,
                                             'Message'] = None) -> 'Message':
        """Send a contact to this user"""
        return self.client.send_contact(
            self.id,
            phone_number,
            first_name,
            last_name,
            reply_markup,
            reply_to_message)

    def send_invoice(self,
                     title: str,
                     description: str,
                     payload: str,
                     provider_token: str,
                     prices: list,
                     photo_url: Optional[str] = None,
                     reply_to_message: Union[int,
                                             str,
                                             'Message'] = None,
                     reply_markup: Union[MenuKeyboardMarkup | InlineKeyboardMarkup] = None):
        return self.client.send_invoice(
            self.id,
            title,
            description,
            payload,
            provider_token,
            prices,
            photo_url,
            reply_to_message,
            reply_markup)