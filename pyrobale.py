"""
PyRobale - A Python library for developing bale bots.

Features:
- Simple and fast
- Customizable and Customized
- New and Up to date
- Internal database management
- Easy to use
- Eazy to learn
"""
from typing import Optional, Dict, Any, List, Union
import os
import json
import time
import threading
import traceback
import sqlite3
import inspect
import re
import sys
import requests
import collections

__version__ = '0.2.9.1'


class ChatActions:
    """Represents different chat action states that can be sent to Bale"""
    TYPING: str = 'typing'
    PHOTO: str = 'upload_photo'
    VIDEO: str = 'record_video'
    CHOOSE_STICKER: str = 'choose_sticker'


class DataBase:
    """
    Database class for managing key-value pairs in a SQLite database.
    """

    def __init__(self, name):
        self.name = name
        self.conn = None
        self.cursor = None
        self._initialize_db()

    def _initialize_db(self):
        self.conn = sqlite3.connect(self.name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS key_value_store
                        (key TEXT PRIMARY KEY, value TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                         updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def read_database(self, include_timestamps=False):
        if not self.conn:
            self._initialize_db()
        if include_timestamps:
            self.cursor.execute(
                "SELECT key, value, created_at, updated_at FROM key_value_store")
            rows = self.cursor.fetchall()
            return {
                key: {
                    'value': json.loads(value),
                    'created_at': created,
                    'updated_at': updated} for key,
                value,
                created,
                updated in rows}
        else:
            self.cursor.execute("SELECT key, value FROM key_value_store")
            rows = self.cursor.fetchall()
            return {key: json.loads(value) for key, value in rows}

    def write_database(self, data_dict):
        if not self.conn:
            self._initialize_db()
        for key, value in data_dict.items():
            self.cursor.execute("""
                INSERT INTO key_value_store (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(key) DO UPDATE SET
                value=excluded.value, updated_at=CURRENT_TIMESTAMP""",
                                (key, json.dumps(value, default=str)))
        self.conn.commit()

    def read_key(self, key: str, default=None):
        if not self.conn:
            self._initialize_db()
        self.cursor.execute(
            "SELECT value FROM key_value_store WHERE key = ?", (key,))
        result = self.cursor.fetchone()
        return json.loads(result[0]) if result else default

    def write_key(self, key: str, value):
        if not self.conn:
            self._initialize_db()
        self.cursor.execute("""
            INSERT INTO key_value_store (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET
            value=excluded.value, updated_at=CURRENT_TIMESTAMP""",
                            (key, json.dumps(value, default=str)))
        self.conn.commit()

    def delete_key(self, key: str):
        if not self.conn:
            self._initialize_db()
        self.cursor.execute(
            "DELETE FROM key_value_store WHERE key = ?", (key,))
        self.conn.commit()

    def keys(self):
        if not self.conn:
            self._initialize_db()
        self.cursor.execute("SELECT key FROM key_value_store")
        return [row[0] for row in self.cursor.fetchall()]

    def clear(self):
        if not self.conn:
            self._initialize_db()
        self.cursor.execute("DELETE FROM key_value_store")
        self.conn.commit()

    def get_metadata(self, key: str):
        if not self.conn:
            self._initialize_db()
        self.cursor.execute("""
            SELECT created_at, updated_at
            FROM key_value_store
            WHERE key = ?""", (key,))
        result = self.cursor.fetchone()
        return {
            'created_at': result[0],
            'updated_at': result[1]} if result else None

    def exists(self, key: str) -> bool:
        if not self.conn:
            self._initialize_db()
        self.cursor.execute(
            "SELECT 1 FROM key_value_store WHERE key = ?", (key,))
        return bool(self.cursor.fetchone())


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


class BaleException(Exception):
    """Base exception for Bale API errors"""

    def __init__(self, message=None, error_code=None, response=None):
        self.message = message
        self.error_code = error_code
        self.response = response

        error_text = f"Error {error_code}: {message}" if error_code and message else message or str(
            error_code)
        super().__init__(error_text)

    def __str__(self):
        error_details = []
        if self.error_code:
            error_details.append(f"code={self.error_code}")
        if self.message:
            error_details.append(f"message='{self.message}'")
        details = ", ".join(error_details)
        return f"{self.__class__.__name__}({details})"


class BaleAPIError(BaleException):
    """Exception raised when Bale API returns an error response"""
    pass


class BaleNetworkError(BaleException):
    """Exception raised when network-related issues occur during API calls"""
    pass


class BaleAuthError(BaleException):
    """Exception raised when authentication fails or token is invalid"""
    pass


class BaleValidationError(BaleException):
    """Exception raised when request data fails validation"""
    pass


class BaleTimeoutError(BaleException):
    """Exception raised when API request times out"""
    pass


class BaleNotFoundError(BaleException):
    """Exception raised when requested resource is not found (404)"""
    pass


class BaleForbiddenError(BaleException):
    """Exception raised when access to resource is forbidden (403)"""
    pass


class BaleServerError(BaleException):
    """Exception raised when server encounters an error (5xx)"""
    pass


class BaleRateLimitError(BaleException):
    """Exception raised when API rate limit is exceeded (429)"""
    pass


class BaleTokenNotFoundError(BaleException):
    """Exception raised when required API token is missing"""
    pass


class BaleUnknownError(BaleException):
    """Exception raised for unexpected or unknown errors"""
    pass


class LabeledPrice:
    def __init__(self, label: str, amount: int):
        self.label = label
        self.amount = amount
        self.json = {
            "label": self.label,
            "amount": self.amount
        }


class Document:
    def __init__(self, data: dict):
        print(data)
        if data:
            self.file_id = data.get('file_id')
            self.file_unique_id = data.get('file_unique_id')
            self.file_name = data.get('file_name')
            self.mime_type = data.get('mime_type')
            self.file_size = data.get('file_size')
            self.input_file = InputFile(self.file_id)
        else:
            self.file_id = None
            self.file_unique_id = None
            self.file_name = None
            self.mime_type = None
            self.file_size = None
            self.input_file = None

    def __bool__(self):
        return bool(self.file_id)


class Invoice:
    def __init__(self, data: dict):
        if data:
            self.title = data.get('title')
            self.description = data.get('description')
            self.start_parameter = data.get('start_parameter')
            self.currency = data.get('currency')
            self.total_amount = data.get('total_amount')
        else:
            self.title = None
            self.description = None
            self.start_parameter = None
            self.currency = None
            self.total_amount = None


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


class Voice:
    def __init__(self, data: dict):
        if data:
            self.file_id = data.get('file_id')
            self.file_unique_id = data.get('file_unique_id')
            self.duration = data.get('duration')
            self.mime_type = data.get('mime_type')
            self.file_size = data.get('file_size')
        else:
            self.file_id = None
            self.file_unique_id = None
            self.duration = None
            self.mime_type = None
            self.file_size = None


class Location:
    def __init__(self, data: dict):
        if data:
            self.long = self.longitude = data.get('longitude')
            self.lat = self.latitude = data.get('latitude')
        else:
            self.longitude = self.long = None
            self.latitude = self.lat = None


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
    def __init__(self, menu_keyboard: Optional[list] = None):
        self.menu_keyboard = []
        if menu_keyboard:
            for row_idx, row in enumerate(menu_keyboard):
                if isinstance(row, tuple) or isinstance(row, str):
                    buttons = [row] if isinstance(row, str) else row
                    for button in buttons:
                        if not isinstance(button, str):
                            raise ValueError("Button must be string")
                        self.add(MenuKeyboardButton(button), row_idx)

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
    def __init__(self, inline_keyboard: Optional[list] = None):
        self.inline_keyboard = []
        if inline_keyboard:
            for row_idx, row in enumerate(inline_keyboard):
                for button in row:
                    if not isinstance(button, (tuple, list)):
                        raise ValueError("Button must be a tuple or list")
                    if len(button) != 2:
                        raise ValueError(
                            "Button must contain exactly text and callback_data/url/web_app")
                    if not isinstance(button[0], str) or not isinstance(
                            button[1], str):
                        raise ValueError(
                            "Button text and data must be strings")
                    self.add(
                        InlineKeyboardButton(
                            button[0],
                            callback_data=button[1]),
                        row_idx)

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


class InputMedia:
    """Base class for input media types"""

    def __init__(self, media: str, caption: str = None):
        self.media = media
        self.caption = caption

    @property
    def media_dict(self) -> dict:
        media_dict = {
            'media': self.media,
            'type': self.type
        }
        if self.caption:
            media_dict['caption'] = self.caption
        return media_dict


class InputMediaPhoto(InputMedia):
    """Represents a photo to be sent"""
    type = 'photo'


class InputMediaVideo(InputMedia):
    """Represents a video to be sent"""
    type = 'video'

    def __init__(self, media: str, caption: str = None, width: int = None,
                 height: int = None, duration: int = None):
        super().__init__(media, caption)
        self.width = width
        self.height = height
        self.duration = duration

    @property
    def media_dict(self) -> dict:
        media_dict = super().media_dict
        if self.width:
            media_dict['width'] = self.width
        if self.height:
            media_dict['height'] = self.height
        if self.duration:
            media_dict['duration'] = self.duration
        return media_dict


class InputMediaAnimation(InputMedia):
    """Represents an animation to be sent"""
    type = 'animation'

    def __init__(self, media: str, caption: str = None, width: int = None,
                 height: int = None, duration: int = None):
        super().__init__(media, caption)
        self.width = width
        self.height = height
        self.duration = duration

    @property
    def media_dict(self) -> dict:
        media_dict = super().media_dict
        if self.width:
            media_dict['width'] = self.width
        if self.height:
            media_dict['height'] = self.height
        if self.duration:
            media_dict['duration'] = self.duration
        return media_dict


class InputFile:
    """Represents a file to be sent"""

    def __init__(self, file: Union[str, bytes] = None, file_id: str = None):
        if file and file_id:
            raise ValueError(
                "Either file or file_id should be provided, not both")
        elif not file and not file_id:
            raise ValueError("Either file or file_id must be provided")

        self.file = file
        self.file_id = file_id

    @property
    def file_type(self) -> str:
        if self.file_id:
            return "id"
        if isinstance(self.file, bytes):
            return "bytes"
        if self.file.startswith(('http://', 'https://')):
            return "url"
        return "path"

    def __str__(self) -> str:
        if self.file_id:
            return self.file_id
        return str(self.file)


class InputMediaAudio(InputMedia):
    """Represents an audio file to be sent"""
    type = 'audio'

    def __init__(self, media: str, caption: str = None, duration: int = None,
                 performer: str = None, title: str = None):
        super().__init__(media, caption)
        self.duration = duration
        self.performer = performer
        self.title = title

    @property
    def media_dict(self) -> dict:
        media_dict = super().media_dict
        if self.duration:
            media_dict['duration'] = self.duration
        if self.performer:
            media_dict['performer'] = self.performer
        if self.title:
            media_dict['title'] = self.title
        return media_dict


class InputMediaDocument(InputMedia):
    """Represents a document to be sent"""
    type = 'document'


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
        self.chat = self.message.chat

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


class Chat:
    """Represents a chat conversation"""

    def __init__(self, client: 'Client', data: Dict[str, Any]):
        if not data.get('ok'):
            raise BaleException(
                f"API request failed: {traceback.format_exc()}")
        self.client = client
        result = data.get('result', {})
        self.data = data
        self.id = result.get('id')
        self.type = result.get('type')
        self.title = result.get('title')
        self.username = result.get('username')
        self.description = result.get('description')
        self.invite_link = result.get('invite_link')
        self.photo = result.get('photo')
        self.is_channel_chat = self.CHANNEL = self.type == "channel"
        self.is_group_chat = self.GROUP = self.type == "group"
        self.is_private_chat = self.PRIVATE = self.type == "private"

    def send_photo(self,
                   photo: Union[str,
                                bytes,
                                InputFile],
                   caption: Optional[str] = None,
                   parse_mode: Optional[str] = None,
                   reply_markup: Union[MenuKeyboardMarkup,
                                       InlineKeyboardMarkup] = None) -> 'Message':
        """Send a photo to a chat"""
        files = None
        data = {
            'chat_id': self.id,
            'caption': caption,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup.keyboard if isinstance(
                reply_markup,
                MenuKeyboardMarkup) else reply_markup.keyboard if isinstance(
                reply_markup,
                InlineKeyboardMarkup) else None}

        if isinstance(photo, (bytes, InputFile)) or hasattr(photo, 'read'):
            files = {
                'photo': photo if not isinstance(
                    photo, InputFile) else photo.file}
        else:
            data['photo'] = photo

        response = self.client._make_request(
            'POST', 'sendPhoto', data=data, files=files)
        return Message(self.client, response)

    def send_message(self,
                     text: str,
                     parse_mode: Optional[str] = None,
                     reply_markup: Union[MenuKeyboardMarkup,
                                         InlineKeyboardMarkup] = None) -> 'Message':
        return self.client.send_message(
            self.id, text, parse_mode, reply_markup)

    def forward_message(
            self, from_chat_id: Union[int, str], message_id: int) -> 'Message':
        """Forward a message from another chat"""
        return self.client.forward_message(self.id, from_chat_id, message_id)

    def copy_message(self,
                     from_chat_id: Union[int,
                                         str],
                     message_id: int,
                     caption: Optional[str] = None,
                     parse_mode: Optional[str] = None,
                     reply_markup: Union[MenuKeyboardMarkup,
                                         InlineKeyboardMarkup] = None) -> 'Message':
        """Copy a message from another chat"""
        return self.client.copy_message(
            self.id,
            from_chat_id,
            message_id,
            caption,
            parse_mode,
            reply_markup)

    def send_audio(self,
                   audio: Union[str,
                                bytes,
                                InputFile],
                   caption: Optional[str] = None,
                   parse_mode: Optional[str] = None,
                   duration: Optional[int] = None,
                   performer: Optional[str] = None,
                   title: Optional[str] = None,
                   reply_markup: Union[MenuKeyboardMarkup,
                                       InlineKeyboardMarkup] = None) -> 'Message':
        """Send an audio file"""
        return self.client.send_audio(
            self.id,
            audio,
            caption,
            parse_mode,
            duration,
            performer,
            title,
            reply_markup)

    def send_document(self,
                      document: Union[str,
                                      bytes,
                                      InputFile],
                      caption: Optional[str] = None,
                      parse_mode: Optional[str] = None,
                      reply_markup: Union[MenuKeyboardMarkup,
                                          InlineKeyboardMarkup] = None) -> 'Message':
        """Send a document"""
        return self.client.send_document(
            self.id, document, caption, parse_mode, reply_markup)

    def send_video(self,
                   video: Union[str,
                                bytes,
                                InputFile],
                   caption: Optional[str] = None,
                   parse_mode: Optional[str] = None,
                   duration: Optional[int] = None,
                   width: Optional[int] = None,
                   height: Optional[int] = None,
                   reply_markup: Union[MenuKeyboardMarkup,
                                       InlineKeyboardMarkup] = None) -> 'Message':
        """Send a video"""
        return self.client.send_video(
            self.id,
            video,
            caption,
            parse_mode,
            duration,
            width,
            height,
            reply_markup)

    def send_animation(self,
                       animation: Union[str,
                                        bytes,
                                        InputFile],
                       caption: Optional[str] = None,
                       parse_mode: Optional[str] = None,
                       duration: Optional[int] = None,
                       width: Optional[int] = None,
                       height: Optional[int] = None,
                       reply_markup: Union[MenuKeyboardMarkup,
                                           InlineKeyboardMarkup] = None) -> 'Message':
        """Send an animation"""
        return self.client.send_animation(
            self.id,
            animation,
            caption,
            parse_mode,
            duration,
            width,
            height,
            reply_markup)

    def send_voice(self,
                   voice: Union[str,
                                bytes,
                                InputFile],
                   caption: Optional[str] = None,
                   parse_mode: Optional[str] = None,
                   duration: Optional[int] = None,
                   reply_markup: Union[MenuKeyboardMarkup,
                                       InlineKeyboardMarkup] = None) -> 'Message':
        """Send a voice message"""
        return self.client.send_voice(
            self.id,
            voice,
            caption,
            parse_mode,
            duration,
            reply_markup)

    def send_media_group(self,
                         chat_id: Union[int,
                                        str],
                         media: List[Dict],
                         reply_to_message: Union['Message',
                                                 int,
                                                 str] = None) -> List['Message']:
        """Send a group of photos, videos, documents or audios as an album"""
        data = {
            'chat_id': chat_id,
            'media': media,
            'reply_to_message_id': reply_to_message.message_id if isinstance(
                reply_to_message,
                Message) else reply_to_message}
        response = self._make_request('POST', 'sendMediaGroup', json=data)
        return [Message(self, msg) for msg in response]

    def send_location(self,
                      latitude: float,
                      longitude: float,
                      live_period: Optional[int] = None,
                      reply_markup: Union[MenuKeyboardMarkup,
                                          InlineKeyboardMarkup] = None) -> 'Message':
        """Send a location"""
        return self.client.send_location(
            self.id, latitude, longitude, live_period, reply_markup)

    def send_contact(self,
                     phone_number: str,
                     first_name: str,
                     last_name: Optional[str] = None,
                     reply_markup: Union[MenuKeyboardMarkup,
                                         InlineKeyboardMarkup] = None) -> 'Message':
        """Send a contact"""
        return self.client.send_contact(
            self.id,
            phone_number,
            first_name,
            last_name,
            reply_markup)

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

    def send_action(self, action: str, how_many_times=1) -> bool:
        """Send a chat action"""
        return self.client.send_chat_action(self.id, action, how_many_times)

    def ban_chat_member(
            self,
            user_id: int,
            until_date: Optional[int] = None) -> bool:
        """Ban a user from the chat"""
        data = {
            'chat_id': self.id,
            'user_id': user_id,
            'until_date': until_date
        }
        response = self.client._make_request(
            'POST', 'banChatMember', data=data)
        return response.get('ok', False)

    def unban_chat_member(
            self,
            user_id: int,
            only_if_banned: bool = False) -> bool:
        """Unban a previously banned user from the chat"""
        data = {
            'chat_id': self.id,
            'user_id': user_id,
            'only_if_banned': only_if_banned
        }
        response = self.client._make_request(
            'POST', 'unbanChatMember', data=data)
        return response.get('ok', False)

    def promotee_chat_member(
            self,
            user_id: int,
            can_change_info: bool = None,
            can_post_messages: bool = None,
            can_edit_messages: bool = None,
            can_delete_messages: bool = None,
            can_manage_video_chats: bool = None,
            can_invite_users: bool = None,
            can_restrict_members: bool = None) -> bool:
        """Promote or demote a chat member"""
        data = {
            'chat_id': self.id,
            'user_id': user_id,
            'can_change_info': can_change_info,
            'can_post_messages': can_post_messages,
            'can_edit_messages': can_edit_messages,
            'can_delete_messages': can_delete_messages,
            'can_manage_video_chats': can_manage_video_chats,
            'can_invite_users': can_invite_users,
            'can_restrict_members': can_restrict_members
        }
        response = self.client._make_request(
            'POST', 'promoteChatMember', data=data)
        return response.get('ok', False)

    def set_chat_photo(self, photo: Union[str, bytes, InputFile]) -> bool:
        """Set a new chat photo"""
        files = None
        data = {'chat_id': self.id}

        if isinstance(photo, (bytes, InputFile)) or hasattr(photo, 'read'):
            files = {
                'photo': photo if not isinstance(
                    photo, InputFile) else photo.file}
        else:
            data['photo'] = photo

        response = self.client._make_request(
            'POST', 'setChatPhoto', data=data, files=files)
        return response.get('ok', False)

    def leave_chat(self) -> bool:
        """Leave the chat"""
        data = {'chat_id': self.id}
        response = self.client._make_request('POST', 'leaveChat', data=data)
        return response.get('ok', False)

    def get_chat(self) -> 'Chat':
        """Get up to date information about the chat"""
        data = {'chat_id': self.id}
        response = self.client._make_request('GET', 'getChat', data=data)
        return Chat(self.client, response)

    def get_members_count(self) -> int:
        """Get the number of members in the chat"""
        data = {'chat_id': self.id}
        response = self.client._make_request(
            'POST', 'getChatMembersCount', data=data)
        return response.get('result', 0)

    def pin_message(
            self,
            message_id: int,
            disable_notification: bool = False) -> bool:
        """Pin a message in the chat"""
        data = {
            'chat_id': self.id,
            'message_id': message_id,
            'disable_notification': disable_notification
        }
        response = self.client._make_request(
            'POST', 'pinChatMessage', data=data)
        return response.get('ok', False)

    def unpin_message(self, message_id: int) -> bool:
        """Unpin a message in the chat"""
        data = {
            'chat_id': self.id,
            'message_id': message_id
        }
        response = self.client._make_request(
            'POST', 'unpinChatMessage', data=data)
        return response.get('ok', False)

    def unpin_all_messages(self) -> bool:
        """Unpin all messages in the chat"""
        data = {'chat_id': self.id}
        response = self.client._make_request(
            'POST', 'unpinAllChatMessages', data=data)
        return response.get('ok', False)

    def set_chat_title(self, title: str) -> bool:
        """Change the title of the chat"""
        data = {
            'chat_id': self.id,
            'title': title
        }
        response = self.client._make_request('POST', 'setChatTitle', data=data)
        return response.get('ok', False)

    def set_chat_description(self, description: str) -> bool:
        """Change the description of the chat"""
        data = {
            'chat_id': self.id,
            'description': description
        }
        response = self.client._make_request(
            'POST', 'setChatDescription', data=data)
        return response.get('ok', False)

    def delete_chat_photo(self) -> bool:
        """Delete the chat photo"""
        data = {'chat_id': self.id}
        response = self.client._make_request(
            'POST', 'deleteChatPhoto', data=data)
        return response.get('ok', False)

    def create_invite_link(self) -> str:
        """Create an invite link for the chat"""
        data = {'chat_id': self.id}
        response = self.client._make_request(
            'POST', 'createChatInviteLink', data=data)
        return response.get('result', {}).get('invite_link')

    def revoke_invite_link(self, invite_link: str) -> bool:
        """Revoke an invite link for the chat"""
        data = {
            'chat_id': self.id,
            'invite_link': invite_link
        }
        response = self.client._make_request(
            'POST', 'revokeChatInviteLink', data=data)
        return response.get('ok', False)

    def export_invite_link(self) -> str:
        """Generate a new invite link for the chat"""
        data = {'chat_id': self.id}
        response = self.client._make_request(
            'POST', 'exportChatInviteLink', data=data)
        return response.get('result')


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

    @property
    def state(self):
        return self.get_state()

    def del_state(self) -> None:
        """Delete the state for a chat or user"""
        self.client.states.pop(str(self.id), None)

    def __str__(self):
        return self.first_name

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

    def send_action(self, action: str, how_many_times: int = 1):
        """Send a chat action to this user"""
        return self.client.send_chat_action(self.id, action, how_many_times)


class Message:
    """Represents a message in Bale"""

    def __init__(self, client: 'Client', data: Dict[str, Any]):
        if not data.get('ok'):
            raise BaleException(
                f"API request failed: {traceback.format_exc()}")
        self.client = client
        self.ok = data.get('ok')
        result = data.get('result', {})
        self.json_result = result

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

        self.document = Document(
            result.get(
                'document',
                {})) if result.get('document') else None

        photos = result.get('photo', [])
        self.photo = [Document(photo) for photo in photos] if photos else None
        self.largest_photo = Document(photos[-1]) if photos else None

        self.video = Document(
            result.get('video')) if result.get('video') else None
        self.audio = Document(
            result.get('audio')) if result.get('audio') else None
        self.voice = Voice(
            result.get('voice')) if result.get('voice') else None
        self.animation = Document(
            result.get('animation')) if result.get('animation') else None
        self.sticker = Document(
            result.get('sticker')) if result.get('sticker') else None
        self.video_note = Document(
            result.get('video_note')) if result.get('video_note') else None

        self.media_group_id = result.get('media_group_id')
        self.has_media = any([self.document,
                              self.photo,
                              self.video,
                              self.audio,
                              self.voice,
                              self.animation,
                              self.sticker,
                              self.video_note])

        self.contact = Contact(
            result.get('contact')) if result.get('contact') else None
        self.location = Location(
            result.get('location')) if result.get('location') else None
        self.forward_from = User(client, {'ok': True, 'result': result.get(
            'forward_from', {})}) if result.get('forward_from') else None
        self.forward_from_message_id = result.get('forward_from_message_id')
        self.invoice = Invoice(
            result.get('invoice')) if result.get('invoice') else None
        self.reply_to_message = Message(client, {'ok': True, 'result': result.get(
            'reply_to_message', {})}) if result.get('reply_to_message') else None
        self.reply = self.reply_message
        self.send = lambda text, parse_mode=None, reply_markup=None: self.client.send_message(
            self.chat.id, text, parse_mode, reply_markup, reply_to_message=self)

        self.command = None
        self.args = None
        txt = self.text.split(' ') if self.text else []

        self.command = txt[0] if txt else None
        self.has_slash_command = self.command.startswith(
            '/') if self.text else None
        self.args = txt[1:] if self.text else None

        self.start = self.command == '/start' if self.text else None

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


class Client:
    """Main client class for interacting with Bale API"""

    def __init__(
            self,
            token: str,
            session: str = 'https://tapi.bale.ai',
            database_name='database.db',
            auto_log_start_message: bool = True,
    ):
        self.token = token
        self.session = session
        self.states = {}
        self.database_name = database_name
        self.auto_log_start_message = auto_log_start_message
        self._base_url = f"{session}/bot{token}"
        self._file_url = f"{session}/file/bot{token}"
        self._session = requests.Session()
        self._message_handler = None
        self._message_edit_handler = None
        self._callback_handler = None
        self._member_leave_handler = None
        self._member_join_handler = None
        self._threads = []
        self._polling = False
        self.user = None

    def set_state(self,
                  chat_or_user_id: Union[Chat,
                                         User,
                                         int,
                                         str],
                  state: str) -> None:
        """Set the state for a chat or user"""
        if isinstance(chat_or_user_id, (Chat, User)):
            chat_or_user_id = chat_or_user_id.id
        self.states[str(chat_or_user_id)] = state

    def get_state(self,
                  chat_or_user_id: Union[Chat,
                                         User,
                                         int,
                                         str]) -> str | None:
        """Get the state for a chat or user"""
        if isinstance(chat_or_user_id, (Chat, User)):
            chat_or_user_id = chat_or_user_id.id
        return self.states.get(str(chat_or_user_id))

    def del_state(self, chat_or_user_id: Union[Chat, User, int, str]) -> None:
        """Delete the state for a chat or user"""
        if isinstance(chat_or_user_id, (Chat, User)):
            chat_or_user_id = chat_or_user_id.id
        self.states.pop(str(chat_or_user_id), None)

    @property
    def database(self) -> DataBase:
        """Get the database name"""
        db = DataBase(self.database_name)
        return db

    def get_chat(self, chat_id: int) -> Optional[Dict]:
        """Get chat information from database"""
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM chats WHERE chat_id = ?', (chat_id,))
        chat = cursor.fetchone()
        conn.close()
        if chat:
            return {
                'chat_id': chat[0],
                'type': chat[1],
                'title': chat[2],
                'created_at': chat[3]
            }
        return None

    def _make_request(self, method: str, endpoint: str,
                      **kwargs) -> Dict[str, Any]:
        """Make an HTTP request to Bale API"""
        url = f"{self._base_url}/{endpoint}"
        response = self._session.request(method, url, **kwargs)
        response_data = response.json()
        if not response_data.get('ok'):
            raise BaleException(
                response_data['error_code'],
                response_data['description'])
        return response_data

    def __del__(self):
        if hasattr(self, '_session'):
            self._session.close()

    def get_me(self) -> User:
        """Get information about the bot"""
        data = self._make_request('GET', 'getMe')
        return User(self, data)

    def get_file(self, file_id: str) -> bytes:
        """Get file information from Bale API"""
        data = {
            'file_id': file_id
        }
        response = self._make_request('POST', 'getFile', json=data)
        file_path = response['result']['file_path']
        url = f"{self._file_url}/{file_path}"
        file_response = self._session.get(url)
        return file_response.content

    def set_webhook(self, url: str, certificate: Optional[str] = None,
                    max_connections: Optional[int] = None) -> bool:
        """Set webhook for getting updates"""
        data = {
            'url': url,
            'certificate': certificate,
            'max_connections': max_connections
        }
        return self._make_request('POST', 'setWebhook', json=data)

    def get_webhook_info(self) -> Dict[str, Any]:
        """Get current webhook status"""
        return self._make_request('GET', 'getWebhookInfo')

    def send_message(self,
                     chat_id: Union[int,
                                    str],
                     text: str,
                     parse_mode: Optional[str] = None,
                     reply_markup: Union[MenuKeyboardMarkup,
                                         InlineKeyboardMarkup] = None,
                     reply_to_message: Union[Message,
                                             int,
                                             str] = None) -> Message:
        """Send a message to a chat"""

        text = str(text)

        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup.keyboard if reply_markup else None,
            'reply_to_message_id': reply_to_message.message_id if isinstance(
                reply_to_message,
                Message) else reply_to_message}
        response = self._make_request('POST', 'sendMessage', json=data)
        return Message(self, response)

    def forward_message(self, chat_id: Union[int, str],
                        from_chat_id: Union[int, str],
                        message_id: int) -> Message:
        """Forward a message from one chat to another"""
        data = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_id': message_id
        }
        response = self._make_request('POST', 'forwardMessage', json=data)
        return Message(self, response)

    def send_photo(self,
                   chat_id: Union[int,
                                  str],
                   photo: Union[str,
                                bytes,
                                InputFile],
                   caption: Optional[str] = None,
                   parse_mode: Optional[str] = None,
                   reply_markup: Union[MenuKeyboardMarkup,
                                       InlineKeyboardMarkup] = None,
                   reply_to_message: Union[Message,
                                           int,
                                           str] = None) -> Message:
        """Send a photo to a chat"""
        files = None
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup.keyboard if reply_markup else None,
            'reply_to_message_id': reply_to_message.message_id if isinstance(
                reply_to_message,
                Message) else reply_to_message}

        if isinstance(photo, (bytes, InputFile)) or hasattr(photo, 'read'):
            files = {
                'photo': photo if not isinstance(
                    photo, InputFile) else photo.file}
        else:
            data['photo'] = photo

        response = self._make_request(
            'POST', 'sendPhoto', data=data, files=files)
        return Message(self, response)

    def delete_message(self, chat_id: Union[int, str],
                       message_id: int) -> bool:
        """Delete a message from a chat"""
        data = {
            'chat_id': chat_id,
            'message_id': message_id
        }
        return self._make_request('POST', 'deleteMessage', json=data)

    def get_user(self, user_id: Union[int, str]) -> User:
        """Get information about a user"""
        data = self._make_request('POST', 'getChat', json={'chat_id': user_id})
        return User(self, data)

    def edit_message(self,
                     chat_id: Union[int,
                                    str],
                     message_id: int,
                     text: str,
                     parse_mode: Optional[str] = None,
                     reply_markup: Union[MenuKeyboardMarkup,
                                         InlineKeyboardMarkup] = None) -> Message:
        """Edit a message in a chat"""
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup.keyboard if reply_markup else None
        }
        response = self._make_request('POST', 'editMessageText', json=data)
        return Message(self, response)

    def get_chat(self, chat_id: Union[int, str]) -> Chat:
        """Get information about a chat"""
        data = self._make_request('POST', 'getChat', json={'chat_id': chat_id})
        return Chat(self, data)

    def send_audio(self,
                   chat_id: Union[int,
                                  str],
                   audio,
                   caption: Optional[str] = None,
                   parse_mode: Optional[str] = None,
                   reply_markup: Union[MenuKeyboardMarkup,
                                       InlineKeyboardMarkup] = None,
                   reply_to_message: Union[Message,
                                           int,
                                           str] = None) -> Message:
        """Send an audio file"""
        files = None
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup.keyboard if reply_markup else None,
            'reply_to_message_id': reply_to_message.message_id if isinstance(
                reply_to_message,
                Message) else reply_to_message}
        if isinstance(audio, (bytes, InputFile)) or hasattr(audio, 'read'):
            files = {
                'audio': audio if not isinstance(
                    audio, InputFile) else audio.file}
        else:
            data['audio'] = audio

        response = self._make_request(
            'POST', 'sendAudio', data=data, files=files)
        return Message(self, response)

    def send_document(self,
                      chat_id: Union[int,
                                     str],
                      document,
                      caption: Optional[str] = None,
                      parse_mode: Optional[str] = None,
                      reply_markup: Union[MenuKeyboardMarkup,
                                          InlineKeyboardMarkup] = None,
                      reply_to_message: Union[Message,
                                              int,
                                              str] = None) -> Message:
        """Send a document"""
        files = None
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup.keyboard if reply_markup else None,
            'reply_to_message_id': reply_to_message.message_id if isinstance(
                reply_to_message,
                Message) else reply_to_message}

        if isinstance(
                document, (bytes, InputFile)) or hasattr(
                document, 'read'):
            files = {'document': document if not isinstance(
                document, InputFile) else document.file}
        else:
            data['document'] = document

        response = self._make_request(
            'POST', 'sendDocument', data=data, files=files)
        return Message(self, response)

    def send_video(self,
                   chat_id: Union[int,
                                  str],
                   video,
                   caption: Optional[str] = None,
                   parse_mode: Optional[str] = None,
                   reply_markup: Union[MenuKeyboardMarkup,
                                       InlineKeyboardMarkup] = None,
                   reply_to_message: Union[Message,
                                           int,
                                           str] = None) -> Message:
        """Send a video"""
        files = None
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup.keyboard if reply_markup else None,
            'reply_to_message_id': reply_to_message.message_id if isinstance(
                reply_to_message,
                Message) else reply_to_message}

        if isinstance(video, (bytes, InputFile)) or hasattr(video, 'read'):
            files = {
                'video': video if not isinstance(
                    video, InputFile) else video.file}
        else:
            data['video'] = video

        response = self._make_request(
            'POST', 'sendVideo', data=data, files=files)
        return Message(self, response)

    def send_animation(self,
                       chat_id: Union[int,
                                      str],
                       animation,
                       caption: Optional[str] = None,
                       parse_mode: Optional[str] = None,
                       reply_markup: Union[MenuKeyboardMarkup,
                                           InlineKeyboardMarkup] = None,
                       reply_to_message: Union[Message,
                                               int,
                                               str] = None) -> Message:
        """Send an animation (GIF or H.264/MPEG-4 AVC video without sound)"""
        files = None
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup.keyboard if reply_markup else None,
            'reply_to_message_id': reply_to_message.message_id if isinstance(
                reply_to_message,
                Message) else reply_to_message}

        if isinstance(
                animation, (bytes, InputFile)) or hasattr(
                animation, 'read'):
            files = {'animation': animation if not isinstance(
                animation, InputFile) else animation.file}
        else:
            data['animation'] = animation

        response = self._make_request(
            'POST', 'sendAnimation', data=data, files=files)
        return Message(self, response)

    def send_voice(self,
                   chat_id: Union[int,
                                  str],
                   voice,
                   caption: Optional[str] = None,
                   parse_mode: Optional[str] = None,
                   reply_markup: Union[MenuKeyboardMarkup,
                                       InlineKeyboardMarkup] = None,
                   reply_to_message: Union[Message,
                                           int,
                                           str] = None) -> Message:
        """Send a voice message"""
        files = None
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup.keyboard if reply_markup else None,
            'reply_to_message_id': reply_to_message.message_id if isinstance(
                reply_to_message,
                Message) else reply_to_message}

        if isinstance(voice, (bytes, InputFile)) or hasattr(voice, 'read'):
            files = {
                'voice': voice if not isinstance(
                    voice, InputFile) else voice.file}
        else:
            data['voice'] = voice

        response = self._make_request(
            'POST', 'sendVoice', data=data, files=files)
        return Message(self, response)

    def send_media_group(self,
                         chat_id: Union[int,
                                        str],
                         media: List[Dict],
                         reply_to_message: Union[Message,
                                                 int,
                                                 str] = None) -> List[Message]:
        """Send a group of photos, videos, documents or audios as an album"""
        data = {
            'chat_id': chat_id,
            'media': media,
            'reply_to_message_id': reply_to_message.message_id if isinstance(
                reply_to_message,
                Message) else reply_to_message}
        response = self._make_request('POST', 'sendMediaGroup', json=data)
        return [Message(self, msg) for msg in response]

    def send_location(self,
                      chat_id: Union[int,
                                     str],
                      latitude: float,
                      longitude: float,
                      reply_markup: Union[MenuKeyboardMarkup,
                                          InlineKeyboardMarkup] = None,
                      reply_to_message: Union[Message,
                                              int,
                                              str] = None) -> Message:
        """Send a point on the map"""
        data = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
            'reply_markup': reply_markup.keyboard if reply_markup else None,
            'reply_to_message_id': reply_to_message.message_id if isinstance(
                reply_to_message,
                Message) else reply_to_message}
        response = self._make_request('POST', 'sendLocation', json=data)
        return Message(self, response)

    def send_contact(self,
                     chat_id: Union[int,
                                    str],
                     phone_number: str,
                     first_name: str,
                     last_name: Optional[str] = None,
                     reply_markup: Union[MenuKeyboardMarkup,
                                         InlineKeyboardMarkup] = None,
                     reply_to_message: Union[Message,
                                             int,
                                             str] = None) -> Message:
        """Send a phone contact"""
        data = {
            'chat_id': chat_id,
            'phone_number': phone_number,
            'first_name': first_name,
            'last_name': last_name,
            'reply_markup': reply_markup.keyboard if reply_markup else None,
            'reply_to_message_id': reply_to_message.message_id if isinstance(
                reply_to_message,
                Message) else reply_to_message}
        response = self._make_request('POST', 'sendContact', json=data)
        return Message(self, response)

    def send_invoice(self,
                     chat_id: Union[int,
                                    str],
                     title: str,
                     description: str,
                     payload: str,
                     provider_token: str,
                     prices: list,
                     photo_url: Optional[str] = None,
                     reply_to_message: Union[int | str | Message] = None,
                     reply_markup: Union[MenuKeyboardMarkup | InlineKeyboardMarkup] = None) -> Message:
        """Send a invoice"""
        r = []
        for x in prices:
            r.append(x.json)
        prices = r
        data = {
            'chat_id': chat_id,
            'title': title,
            'description': description,
            'payload': payload,
            'provider_token': provider_token,
            'prices': prices,
            'photo_url': photo_url,
            'reply_to_message_id': reply_to_message.message_id if isinstance(
                reply_to_message,
                Message) else reply_to_message,
            'reply_markup': reply_markup.keyboard if reply_markup else None}
        response = self._make_request('POST', 'sendInvoice', json=data)
        return Message(self, response)

    def send_chat_action(self,
                         chat: Union[int,
                                     str,
                                     'Chat'],
                         action: str,
                         how_many_times: int = 1) -> bool:
        """Send a chat action"""
        if not chat:
            raise ValueError("Chat ID cannot be empty")

        data = {
            'chat_id': str(chat) if isinstance(
                chat, (int, str)) else str(
                chat.id), 'action': action}
        res = []
        for _ in range(how_many_times):
            response = self._make_request('POST', 'sendChatAction', json=data)
            res.append(response.get('ok', False))
        return all(res)

    def copy_message(self,
                     chat_id: Union[int,
                                    str,
                                    'Chat'],
                     from_chat_id: Union[int,
                                         str,
                                         'Chat'],
                     message_id: Union[int,
                                       str,
                                       'Chat']):
        data = {
            'chat_id': chat_id if isinstance(
                chat_id, (int, str)) else chat_id.id, 'from_chat_id': from_chat_id if isinstance(
                from_chat_id, (int, str)) else from_chat_id.id, 'message_id': message_id if isinstance(
                message_id, (int, str)) else message_id.id}
        response = self._make_request('POST', 'copyMessage', json=data)
        return Message(self, response)

    def get_chat_member(self,
                        chat: Union[int,
                                    str,
                                    'Chat'],
                        user: Union[int,
                                    str,
                                    'User']) -> ChatMember:
        """Get information about a member of a chat including their permissions"""
        data = {
            'chat_id': chat if isinstance(chat, (int, str)) else chat.id,
            'user_id': user if isinstance(user, (int, str)) else user.id
        }
        response = self._make_request('POST', 'getChatMember', json=data)
        return ChatMember(self, response['result'])

    def get_chat_administrators(
            self, chat: Union[int, str, 'Chat']) -> List[ChatMember]:
        """Get a list of administrators in a chat"""
        data = {'chat_id': getattr(chat, 'id', chat)}
        response = self._make_request(
            'POST', 'getChatAdministrators', json=data)
        return [ChatMember(self, member)
                for member in response.get('result', [])]

    def get_chat_members_count(self, chat: Union[int, str, 'Chat']) -> int:
        """Get the number of members in a chat"""
        data = {
            'chat_id': chat if isinstance(chat, (int, str)) else chat.id
        }
        response = self._make_request('GET', 'getChatMembersCount', json=data)
        return response['result']

    def is_joined(self, user: Union[User, int, str],
                  chat: Union[Chat, int, str]) -> bool:
        """Check if user is a member of the chat"""
        data = {
            'chat_id': chat if isinstance(chat, (int, str)) else chat.id,
            'user_id': user if isinstance(user, (int, str)) else user.id
        }
        response = self._make_request('GET', 'getChatMember', json=data)
        return response.get('status') not in ['left', 'kicked']

    def on_message(self, func):
        """Decorator for handling new messages"""
        self._message_handler = func
        return func

    def on_callback_query(self, func):
        """Decorator for handling callback queries"""
        self._callback_handler = func
        return func

    def on_tick(self, seconds: int):
        """Decorator for handling periodic events"""
        def decorator(func):
            if not hasattr(self, '_tick_handlers'):
                self._tick_handlers = {}
            self._tick_handlers[func] = {
                'interval': seconds, 'last_run': time.time()}
            return func
        return decorator

    def on_close(self, func):
        """Decorator for handling close event"""
        self._close_handler = func
        return func

    def on_ready(self, func):
        """Decorator for handling ready event"""
        self._ready_handler = func
        return func

    def on_update(self, func):
        """Decorator for handling raw updates"""
        self._update_handler = func
        return func

    def on_member_chat_join(self, func):
        """Decorator for handling new chat members"""
        self._member_join_handler = func
        return func

    def on_member_chat_leave(self, func):
        """Decorator for handling members leaving chat"""
        self._member_leave_handler = func
        return func

    def on_message_edit(self, func):
        """Decorator for handling edited messages"""
        self._message_edit_handler = func
        return func

    def on_command(self, command: str = None, case_sensitive: bool = False):
        """Decorator for handling specific text commands"""
        def decorator(func):
            if not hasattr(self, '_text_handlers'):
                self._text_handlers = {}
            cmd = f"/{command.lstrip('/')}" if command else f"/{func.__name__}"
            self._text_handlers[cmd] = {
                'handler': func, 'case_sensitive': case_sensitive}
            return func
        return decorator

    def _create_thread(self, handler, *args, **kwargs):
        """Helper method to create and start a thread"""
        if handler:
            thread = threading.Thread(
                target=handler, args=args, kwargs=kwargs, daemon=True)
            thread.start()
            self._threads.append(thread)
            return thread
        return None

    def _handle_message(self, message, update):
        """Handle different types of messages"""
        msg_data = update.get('message', {})

        if 'new_chat_members' in msg_data and hasattr(
                self, '_member_join_handler'):
            chat, user = msg_data['chat'], msg_data['new_chat_members'][0]
            self._create_thread(
                self._member_join_handler,
                message,
                Chat(self, {"ok": True, "result": chat}),
                User(self, {"ok": True, "result": user})
            )
            return

        if 'left_chat_member' in msg_data and hasattr(
                self, '_member_leave_handler'):
            chat, user = msg_data['chat'], msg_data['left_chat_member']
            self._create_thread(
                self._member_leave_handler,
                message,
                Chat(self, {"ok": True, "result": chat}),
                User(self, {"ok": True, "result": user})
            )
            return

        if 'text' in msg_data and hasattr(self, '_text_handlers'):
            text = msg_data['text']
            for command, handler_info in self._text_handlers.items():
                handler = handler_info['handler']
                case_sensitive = handler_info['case_sensitive']

                if case_sensitive:
                    matches = text.startswith(command)
                else:
                    matches = text.lower().startswith(command.lower())

                if matches:
                    params = inspect.signature(handler).parameters
                    args = [message]
                    if len(params) > 1:
                        command_args = text[len(command):].strip().split()
                        args.extend(command_args)
                    self._create_thread(handler, *args)
                    return

        if hasattr(self, '_message_handler'):
            params = inspect.signature(self._message_handler).parameters
            args = ((message, update) if len(params) > 1 else (message,))
            result = self._message_handler(*args)
            if isinstance(result, str):
                message.chat.send_message(result)

    def _handle_update(self, update):
        try:
            if hasattr(self, '_update_handler'):
                self._create_thread(self._update_handler, update)

            message_types = {
                'message': (Message, self._handle_message),
                'edited_message': (Message, lambda m, u: self._create_thread(
                    self._message_edit_handler, m) if hasattr(
                    self, '_message_edit_handler') else None)
            }

            for update_type, (cls, handler) in message_types.items():
                if update_type in update:
                    message = cls(
                        self, {
                            'ok': True, 'result': update[update_type]})
                    handler(message, update)

            if 'callback_query' in update and hasattr(
                    self, '_callback_handler'):
                callback_data = update['callback_query']
                obj = CallbackQuery(
                    self, {'ok': True, 'result': callback_data})
                message = Message(
                    self, {
                        'ok': True, 'result': callback_data['message']}) if 'message' in callback_data else None
                chat = Chat(
                    self, {
                        'ok': True, 'result': callback_data['message']['chat']}) if message else None
                user = User(
                    self, {
                        'ok': True, 'result': callback_data['from']})

                params = inspect.signature(self._callback_handler).parameters
                args = (
                    obj,
                    message,
                    chat,
                    user) if len(params) > 1 else (
                    obj,
                )
                self._create_thread(self._callback_handler, *args)
        except Exception as e:
            print(f"Error handling update: {e}")
            traceback.print_exc()

    def _handle_tick_events(self, current_time):
        """Handle periodic tick events"""
        if hasattr(self, '_tick_handlers'):
            for handler, info in self._tick_handlers.items():
                if current_time - info['last_run'] >= info['interval']:
                    self._create_thread(handler)
                    info['last_run'] = current_time

    def run(self, debug=False):
        """Start polling for new messages"""
        try:
            self.user = self.get_me()
        except Exception as e:
            raise BaleTokenNotFoundError(f"Token not found: {str(e)}")

        self._polling = True
        self._threads = []
        offset = 0
        past_updates = collections.deque(maxlen=100)
        source_file = inspect.getfile(self.__class__)
        last_modified = os.path.getmtime(source_file)

        if self.auto_log_start_message:
            print(f"-+-+-+ [logged in as @{self.get_me().username}] +-+-+-")
        if hasattr(self, '_ready_handler'):
            self._ready_handler()

        while self._polling:
            try:
                if debug and self._check_source_file_changed(
                        source_file, last_modified):
                    last_modified = os.path.getmtime(source_file)
                    print("Source file changed, restarting...")
                    python = sys.executable
                    os.execl(python, python, *sys.argv)

                updates = self.get_updates(offset=offset, timeout=30)
                for update in updates:
                    update_id = update['update_id']
                    if update_id not in past_updates:
                        past_updates.append(update_id)
                        self._handle_update(update)
                        offset = update_id + 1

                current_time = time.time()
                self._handle_tick_events(current_time)
                self._threads = [t for t in self._threads if t.is_alive()]
                time.sleep(0.1)
            except Exception as e:
                print(f"Error in polling: {e}")
                traceback.print_exc()
                time.sleep(1)

    def _check_source_file_changed(self, source_file, last_modified):
        """Check if source file has been modified"""
        try:
            return os.path.getmtime(source_file) > last_modified
        except (FileNotFoundError, OSError) as e:
            print(f"Error checking file modification time: {e}")
            return False

    def get_updates(self, offset=None, timeout=30) -> List[Dict[str, Any]]:
        """Get updates from Bale API"""
        params = {'timeout': timeout}
        if offset is not None:
            params['offset'] = offset
        response = self._make_request('GET', 'getUpdates', params=params)
        return response.get('result', [])

    def safe_close(self):
        """Close the client and stop polling gracefully"""
        self._polling = False
        for thread in self._threads:
            try:
                thread.join(timeout=1.0)
            except Exception as e:
                print(f"Error joining thread: {e}")
        self._threads.clear()
        if hasattr(self, '_close_handler'):
            try:
                self._close_handler()
            except Exception as e:
                print(f"Error in close handler: {e}")

    def create_ref_link(self, data: str) -> str:
        """Create a reference link for the bot"""
        return f"https://ble.ir/{self.get_me().username}?start={data}"


def run_multiple_bots(bots: List[Client]):
    """Run multiple bots in separate threads"""
    threads = []
    for bot in bots:
        thread = threading.Thread(target=bot.run)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    return bots


def stop_bots(bots: List[Client]):
    """Stop multiple bots gracefully"""
    for bot in bots:
        bot.safe_close()
