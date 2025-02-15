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
from ..objects.user import (User)
from ..objects.location import (Location)
from ..objects.contact import (Contact)
from ..objects.database import (DataBase)
from ..objects.inputfile import(InputFile)
from ..objects.labeledprice import (LabeledPrice)
from ..objects.invoice import (Invoice)
from ..objects.client import (Client)
from ..objects.chatmember import (ChatMember)

class Message:
    """Represents a message in Bale"""

    def __init__(self, client: 'Client', data: Dict[str, Any]):
        if not data.get('ok'):
            raise BaleException(
                f"API request failed: {traceback.format_exc()}")
        self.client = client
        self.ok = data.get('ok')
        result = data.get('result', {})

        self.message_id = self.id = result.get('message_id')
        self.from_user = self.author = User(
            client, {'ok': True, 'result': result.get('from', {})})
        self.date = result.get('date')
        self.chat = Chat(
            client, {
                'ok': True, 'result': result.get(
                    'chat', {})})
        self.text = result.get('text')
        self.caption = result.get('caption')
        self.document = Document(result.get('document'))
        self.photo = Document(result.get('photo'))
        self.video = Document(result.get('video'))
        self.audio = Document(result.get('audio'))
        self.voice = Voice(result.get('voice'))
        self.animation = result.get('animation')
        self.contact = Contact(result.get('contact'))
        self.location = Location(result.get('location'))
        self.forward_from = User(
            client, {
                'ok': True, 'result': result.get(
                    'forward_from', {})})
        self.forward_from_message_id = result.get('forward_from_message_id')
        self.invoice = Invoice(result.get('invoice'))
        self.reply = self.reply_message
        self.send = lambda text, parse_mode=None, reply_markup=None: self.client.send_message(
            self.chat.id, text, parse_mode, reply_markup, reply_to_message=self)

    def edit(self,
             text: str,
             parse_mode: Optional[str] = None,
             reply_markup: Union[MenuKeyboardMarkup,
                                 InlineKeyboardMarkup] = None) -> 'Message':
        """Edit this message"""
        return self.client.edit_message(
            self.chat.id,
            self.message_id,
            text,
            parse_mode,
            reply_markup)

    def delete(self) -> bool:
        """Delete this message"""
        return self.client.delete_message(self.chat.id, self.message_id)

    def reply_message(self,
                      text: str,
                      parse_mode: Optional[str] = None,
                      reply_markup: Union[MenuKeyboardMarkup,
                                          InlineKeyboardMarkup] = None) -> 'Message':
        """Send a message to this user"""
        return self.client.send_message(
            self.chat.id,
            text,
            parse_mode,
            reply_markup,
            reply_to_message=self)

    def reply_photo(self,
                    photo: Union[str,
                                 bytes,
                                 InputFile],
                    caption: Optional[str] = None,
                    parse_mode: Optional[str] = None,
                    reply_markup: Union[MenuKeyboardMarkup,
                                        InlineKeyboardMarkup] = None) -> 'Message':
        """Send a photo to a chat"""
        return self.client.send_photo(
            self.chat.id,
            photo,
            caption,
            parse_mode,
            reply_markup,
            reply_to_message=self)

    def reply_audio(self,
                    audio: Union[str,
                                 bytes,
                                 InputFile],
                    caption: Optional[str] = None,
                    parse_mode: Optional[str] = None,
                    reply_markup: Union[MenuKeyboardMarkup,
                                        InlineKeyboardMarkup] = None) -> 'Message':
        """Send an audio file to this user"""
        self.client.send_audio(
            self.chat.id,
            audio,
            caption,
            parse_mode,
            reply_markup,
            reply_to_message=self)

    def reply_document(self,
                       document: Union[str,
                                       bytes,
                                       InputFile],
                       caption: Optional[str] = None,
                       parse_mode: Optional[str] = None,
                       reply_markup: Union[MenuKeyboardMarkup,
                                           InlineKeyboardMarkup] = None) -> 'Message':
        """Send a document to this user"""
        self.client.send_document(
            self.chat.id,
            document,
            caption,
            parse_mode,
            reply_markup,
            reply_markup,
            reply_to_message=self)

    def reply_video(self,
                    video: Union[str,
                                 bytes,
                                 InputFile],
                    caption: Optional[str] = None,
                    parse_mode: Optional[str] = None,
                    reply_markup: Union[MenuKeyboardMarkup,
                                        InlineKeyboardMarkup] = None) -> 'Message':
        """Send a video to this user"""
        self.client.send_video(
            self.chat.id,
            video,
            caption,
            parse_mode,
            reply_markup,
            reply_to_message=self)

    def reply_animation(self,
                        animation: Union[str,
                                         bytes,
                                         InputFile],
                        caption: Optional[str] = None,
                        parse_mode: Optional[str] = None,
                        reply_markup: Union[MenuKeyboardMarkup,
                                            InlineKeyboardMarkup] = None) -> 'Message':
        """Send an animation to this user"""
        return self.client.send_animation(
            self.chat.id,
            animation,
            caption,
            parse_mode,
            reply_markup,
            reply_to_message=self)

    def reply_voice(self,
                    voice: Union[str,
                                 bytes,
                                 InputFile],
                    caption: Optional[str] = None,
                    parse_mode: Optional[str] = None,
                    reply_markup: Union[MenuKeyboardMarkup,
                                        InlineKeyboardMarkup] = None) -> 'Message':
        """Send a voice message to this user"""
        return self.client.send_voice(
            self.chat.id,
            voice,
            caption,
            parse_mode,
            reply_markup,
            reply_to_message=self)

    def reply_media_group(self,
                          media: List[Dict],
                          reply_to_message: Union['Message',
                                                  int,
                                                  str] = None) -> List['Message']:
        """Send a group of photos, videos, documents or audios as an album"""
        return self.client.send_media_group(
            self.chat.id, media, reply_to_message=self)

    def reply_location(self,
                       latitude: float,
                       longitude: float,
                       reply_markup: Union[MenuKeyboardMarkup,
                                           InlineKeyboardMarkup] = None) -> 'Message':
        """Send a location to this user"""
        return self.client.send_location(
            self.chat.id,
            latitude,
            longitude,
            reply_markup,
            reply_to_message=self)

    def reply_contact(self,
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
            self.chat.id,
            phone_number,
            first_name,
            last_name,
            reply_markup,
            reply_to_message)

    def reply_invoice(self,
                      title: str,
                      description: str,
                      payload: str,
                      provider_token: str,
                      prices: list,
                      photo_url: Optional[str] = None,
                      reply_markup: Union[MenuKeyboardMarkup | InlineKeyboardMarkup] = None):
        return self.client.send_invoice(
            self.chat.id,
            title,
            description,
            payload,
            provider_token,
            prices,
            photo_url,
            self,
            reply_markup)