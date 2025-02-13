import requests, json, time, threading
from typing import Optional, Dict, Any, List, Union
import traceback
import sqlite3
import inspect
import asyncio

__version__ = '0.2.3'

class DataBase:
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
            self.cursor.execute("SELECT key, value, created_at, updated_at FROM key_value_store")
            rows = self.cursor.fetchall()
            return {key: {'value': json.loads(value), 'created_at': created, 'updated_at': updated} 
                   for key, value, created, updated in rows}
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
        self.cursor.execute("SELECT value FROM key_value_store WHERE key = ?", (key,))
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
        self.cursor.execute("DELETE FROM key_value_store WHERE key = ?", (key,))
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
        return {'created_at': result[0], 'updated_at': result[1]} if result else None
        
    def exists(self, key: str) -> bool:
        if not self.conn:
            self._initialize_db()
        self.cursor.execute("SELECT 1 FROM key_value_store WHERE key = ?", (key,))
        return bool(self.cursor.fetchone())


class ChatMember:
    def __init__(self, client: 'Client', data: Dict[str, Any]):
        if data:
            self.status = data.get('status')
            self.user = User(client, {'ok': True, 'result': data.get('user', {})})
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
    def __init__(self, *args):
        super().__init__(*args)
        print(traceback.format_exc())
        
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
        if data:
            self.file_id = data.get('file_id')
            self.file_unique_id = data.get('file_unique_id')
            self.file_name = data.get('file_name')
            self.mime_type = data.get('mime_type')
            self.file_size = data.get('file_size')
        else:
            self.file_id = None
            self.file_unique_id = None
            self.file_name = None
            self.mime_type = None
            self.file_size = None

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
    def __init__(self,data):
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
    def __init__(self,data: dict):
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
    def __init__(self, text: str, request_contact: bool = False, request_location: bool = False):
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
    def __init__(self, text: str, callback_data: Optional[str] = None, url: Optional[str] = None, web_app: Optional[str] = None):
        self.button = {"text": text}
        if sum(bool(x) for x in [callback_data, url, web_app]) != 1:
            raise ValueError("Exactly one of callback_data, url, or web_app must be provided")
        if callback_data:
            self.button["callback_data"] = callback_data
        elif url:
            self.button["url"] = url
        elif web_app:
            self.button["web_app"] = {"url": web_app}

class MenuKeyboardMarkup:
    def __init__(self):
        self.menu_keyboard = []

    def add(self, button: MenuKeyboardButton, row: int = 0) -> 'MenuKeyboardMarkup':
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

    def add(self, button: InlineKeyboardButton, row: int = 0) -> 'InlineKeyboardMarkup':
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
class InputFile:
    """Represents a file to be uploaded"""
    def __init__(self, client: 'Client', file: Union[str, bytes], filename: Optional[str] = None):
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
                except IOError as e:
                    raise BaleException(f"Failed to open file: {traceback.format_exc()}")
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

class CallbackQuery:
    """Represents a callback query from a callback button"""
    def __init__(self, client: 'Client', data: Dict[str, Any]):
        if not data.get('ok'):
            raise BaleException(f"API request failed: {traceback.format_exc()}")
        self.client = client
        result = data.get('result', {})
        self.id = result.get('id')
        self.from_user = self.user = self.author = User(client, {'ok': True, 'result': result.get('from', {})})
        self.message = Message(client, {'ok': True, 'result': result.get('message', {})})
        self.inline_message_id = result.get('inline_message_id')
        self.chat_instance = result.get('chat_instance')
        self.data = result.get('data')
    
    def answer(self, text: str, reply_markup: Optional[Union[MenuKeyboardMarkup, InlineKeyboardMarkup]] = None) -> 'Message':
        return self.client.send_message(chat_id=self.message.chat.id, text=text, reply_markup=reply_markup)
    
    def reply(self, text: str, reply_markup: Optional[Union[MenuKeyboardMarkup, InlineKeyboardMarkup]] = None) -> 'Message':
        return self.client.send_message(chat_id=self.message.chat.id, text=text, reply_markup=reply_markup, reply_to_message=self.message.id)


class Chat:
    """Represents a chat conversation"""
    def __init__(self, client: 'Client', data: Dict[str, Any]):
        if not data.get('ok'):
            raise BaleException(f"API request failed: {traceback.format_exc()}")
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

    def send_photo(self, photo: Union[str, bytes, InputFile],
                  caption: Optional[str] = None,
                  parse_mode: Optional[str] = None,
                  reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
        """Send a photo to a chat"""
        files = None
        data = {
            'chat_id': self.id,
            'caption': caption,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup.keyboard if isinstance(reply_markup, MenuKeyboardMarkup) else reply_markup.keyboard if isinstance(reply_markup, InlineKeyboardMarkup) else None
        }
        
        if isinstance(photo, (bytes, InputFile)) or hasattr(photo, 'read'):
            files = {'photo': photo if not isinstance(photo, InputFile) else photo.file}
        else:
            data['photo'] = photo
            
        response = self.client._make_request('POST', 'sendPhoto', data=data, files=files)
        return Message(self.client, response)    

    def send_message(self, text: str,
                    parse_mode: Optional[str] = None,
                    reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
        return self.client.send_message(self.id, text, parse_mode, reply_markup)
    
    def forward_message(self, from_chat_id: Union[int, str], message_id: int) -> 'Message':
            """Forward a message from another chat"""
            return self.client.forward_message(self.id, from_chat_id, message_id)
    
    def copy_message(self, from_chat_id: Union[int, str], message_id: int,
                        caption: Optional[str] = None,
                        parse_mode: Optional[str] = None,
                        reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
            """Copy a message from another chat"""
            return self.client.copy_message(self.id, from_chat_id, message_id, caption, parse_mode, reply_markup)
    
    def send_audio(self, audio: Union[str, bytes, InputFile],
                      caption: Optional[str] = None,
                      parse_mode: Optional[str] = None,
                      duration: Optional[int] = None,
                      performer: Optional[str] = None,
                      title: Optional[str] = None,
                      reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
            """Send an audio file"""
            return self.client.send_audio(self.id, audio, caption, parse_mode, duration, performer, title, reply_markup)
    
    def send_document(self, document: Union[str, bytes, InputFile],
                         caption: Optional[str] = None,
                         parse_mode: Optional[str] = None,
                         reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
            """Send a document"""
            return self.client.send_document(self.id, document, caption, parse_mode, reply_markup)
    
    def send_video(self, video: Union[str, bytes, InputFile],
                      caption: Optional[str] = None,
                      parse_mode: Optional[str] = None,
                      duration: Optional[int] = None,
                      width: Optional[int] = None,
                      height: Optional[int] = None,
                      reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
            """Send a video"""
            return self.client.send_video(self.id, video, caption, parse_mode, duration, width, height, reply_markup)
    
    def send_animation(self, animation: Union[str, bytes, InputFile],
                          caption: Optional[str] = None,
                          parse_mode: Optional[str] = None,
                          duration: Optional[int] = None,
                          width: Optional[int] = None,
                          height: Optional[int] = None,
                          reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
            """Send an animation"""
            return self.client.send_animation(self.id, animation, caption, parse_mode, duration, width, height, reply_markup)
    
    def send_voice(self, voice: Union[str, bytes, InputFile],
                      caption: Optional[str] = None,
                      parse_mode: Optional[str] = None,
                      duration: Optional[int] = None,
                      reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
            """Send a voice message"""
            return self.client.send_voice(self.id, voice, caption, parse_mode, duration, reply_markup)
    
    def send_media_group(self, chat_id: Union[int, str],
                            media: List[Dict],
                            reply_to_message: Union['Message', int, str] = None) -> List['Message']:
            """Send a group of photos, videos, documents or audios as an album"""
            data = {
                'chat_id': chat_id,
                'media': media,
                'reply_to_message_id': reply_to_message.message_id if isinstance(reply_to_message, Message) else reply_to_message
            }
            response = self._make_request('POST', 'sendMediaGroup', json=data)
            return [Message(self, msg) for msg in response]
    
    def send_location(self, latitude: float, longitude: float,
                         live_period: Optional[int] = None,
                         reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
            """Send a location"""
            return self.client.send_location(self.id, latitude, longitude, live_period, reply_markup)
    
    def send_contact(self, phone_number: str, first_name: str,
                        last_name: Optional[str] = None,
                        reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
            """Send a contact"""
            return self.client.send_contact(self.id, phone_number, first_name, last_name, reply_markup)
    
    def send_invoice(self,title:str,description:str,payload:str,provider_token:str,prices:list,photo_url: Optional[str] = None,reply_to_message: Union[int,str,'Message'] = None, reply_markup: Union[MenuKeyboardMarkup|InlineKeyboardMarkup] = None):
        return self.client.send_invoice(self.id,title,description,payload,provider_token,prices,photo_url,reply_to_message,reply_markup)
    
    def banChatMember(self, user_id: int, until_date: Optional[int] = None) -> bool:
        """Ban a user from the chat"""
        data = {
            'chat_id': self.id,
            'user_id': user_id,
            'until_date': until_date
        }
        response = self.client._make_request('POST', 'banChatMember', data=data)
        return response.get('ok', False)

    def unbanChatMember(self, user_id: int, only_if_banned: bool = False) -> bool:
        """Unban a previously banned user from the chat"""
        data = {
            'chat_id': self.id,
            'user_id': user_id,
            'only_if_banned': only_if_banned
        }
        response = self.client._make_request('POST', 'unbanChatMember', data=data)
        return response.get('ok', False)

    def promoteChatMember(self, user_id: int, can_change_info: bool = None,
                         can_post_messages: bool = None, can_edit_messages: bool = None,
                         can_delete_messages: bool = None, can_manage_video_chats: bool = None,
                         can_invite_users: bool = None, can_restrict_members: bool = None) -> bool:
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
        response = self.client._make_request('POST', 'promoteChatMember', data=data)
        return response.get('ok', False)
    
    def setChatPhoto(self, photo: Union[str, bytes, InputFile]) -> bool:
        """Set a new chat photo"""
        files = None
        data = {'chat_id': self.id}
        
        if isinstance(photo, (bytes, InputFile)) or hasattr(photo, 'read'):
            files = {'photo': photo if not isinstance(photo, InputFile) else photo.file}
        else:
            data['photo'] = photo
            
        response = self.client._make_request('POST', 'setChatPhoto', data=data, files=files)
        return response.get('ok', False)

    def leaveChat(self) -> bool:
        """Leave the chat"""
        data = {'chat_id': self.id}
        response = self.client._make_request('POST', 'leaveChat', data=data)
        return response.get('ok', False)

    def getChat(self) -> 'Chat':
        """Get up to date information about the chat"""
        data = {'chat_id': self.id}
        response = self.client._make_request('GET', 'getChat', data=data)
        return Chat(self.client, response)

    def getChatMembersCount(self) -> int:
        """Get the number of members in the chat"""
        data = {'chat_id': self.id}
        response = self.client._make_request('POST', 'getChatMembersCount', data=data)
        return response.get('result', 0)

    def pinChatMessage(self, message_id: int, disable_notification: bool = False) -> bool:
        """Pin a message in the chat"""
        data = {
            'chat_id': self.id,
            'message_id': message_id,
            'disable_notification': disable_notification
        }
        response = self.client._make_request('POST', 'pinChatMessage', data=data)
        return response.get('ok', False)

    def unPinChatMessage(self, message_id: int) -> bool:
        """Unpin a message in the chat"""
        data = {
            'chat_id': self.id,
            'message_id': message_id
        }
        response = self.client._make_request('POST', 'unpinChatMessage', data=data)
        return response.get('ok', False)

    def unpinAllChatMessages(self) -> bool:
        """Unpin all messages in the chat"""
        data = {'chat_id': self.id}
        response = self.client._make_request('POST', 'unpinAllChatMessages', data=data)
        return response.get('ok', False)

    def setChatTitle(self, title: str) -> bool:
        """Change the title of the chat"""
        data = {
            'chat_id': self.id,
            'title': title
        }
        response = self.client._make_request('POST', 'setChatTitle', data=data)
        return response.get('ok', False)

    def setChatDescription(self, description: str) -> bool:
        """Change the description of the chat"""
        data = {
            'chat_id': self.id,
            'description': description
        }
        response = self.client._make_request('POST', 'setChatDescription', data=data)
        return response.get('ok', False)

    def deleteChatPhoto(self) -> bool:
        """Delete the chat photo"""
        data = {'chat_id': self.id}
        response = self.client._make_request('POST', 'deleteChatPhoto', data=data)
        return response.get('ok', False)

    def createChatInviteLink(self) -> str:
        """Create an invite link for the chat"""
        data = {'chat_id': self.id}
        response = self.client._make_request('POST', 'createChatInviteLink', data=data)
        return response.get('result', {}).get('invite_link')

    def revokeChatInviteLink(self, invite_link: str) -> bool:
        """Revoke an invite link for the chat"""
        data = {
            'chat_id': self.id,
            'invite_link': invite_link
        }
        response = self.client._make_request('POST', 'revokeChatInviteLink', data=data)
        return response.get('ok', False)

    def exportChatInviteLink(self) -> str:
        """Generate a new invite link for the chat"""
        data = {'chat_id': self.id}
        response = self.client._make_request('POST', 'exportChatInviteLink', data=data)
        return response.get('result')

    

class User:
    """Represents a Bale user"""
    def __init__(self, client: 'Client', data: Dict[str, Any]):
        if not data.get('ok'):
            raise BaleException(f"API request failed: {traceback.format_exc()}")
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
    
    def get_state(self) -> str|None:
        """Get the state for a chat or user"""
        return self.client.states.get(str(self.id))
    
    def del_state(self) -> None:
        """Delete the state for a chat or user"""
        self.client.states.pop(str(self.id), None)
    

    def send_message(self, text: str, parse_mode: Optional[str] = None, 
                    reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
        """Send a message to this user"""
        return self.client.send_message(self.id, text, parse_mode, reply_markup)
        
    def send_photo(self, photo: Union[str, bytes, InputFile],
                  caption: Optional[str] = None,
                  parse_mode: Optional[str] = None,
                  reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
        """Send a photo to a chat"""
        return self.client.send_photo(self.id, photo, caption, parse_mode, reply_markup)
    
    def forward_message(self, from_chat_id: Union[int, str], message_id: int) -> 'Message':
            """Forward a message to this user"""
            self.client.forward_message(self.id,from_chat_id,message_id)
    
    def copy_message(self, from_chat_id: Union[int, str], message_id: int) -> 'Message':
            """Copy a message to this user"""
            self.client.copy_message(self.id,from_chat_id,message_id)
    
    def send_audio(self, audio: Union[str, bytes, InputFile],
                      caption: Optional[str] = None,
                      parse_mode: Optional[str] = None,
                      reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None, reply_to_message: Union[str,int,'Message'] = None) -> 'Message':
            """Send an audio file to this user"""
            self.client.send_audio(self.id, audio, caption, parse_mode, reply_markup, reply_to_message)
    
    def send_document(self, document: Union[str, bytes, InputFile],
                         caption: Optional[str] = None,
                         parse_mode: Optional[str] = None,
                         reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None, reply_to_message: Union[str,int,'Message'] = None) -> 'Message':
            """Send a document to this user"""
            self.client.send_document(self.id, document, caption, parse_mode, reply_markup, reply_markup)
    
    def send_video(self, video: Union[str, bytes, InputFile],
                      caption: Optional[str] = None,
                      parse_mode: Optional[str] = None,
                      reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None, reply_to_message: Union[str,int,'Message'] = None) -> 'Message':
            """Send a video to this user"""
            self.client.send_video(self.id,video,caption,parse_mode,reply_markup,reply_to_message)
    
    def send_animation(self, animation: Union[str, bytes, InputFile],
                          caption: Optional[str] = None,
                          parse_mode: Optional[str] = None,
                          reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None, reply_to_message: Union[int,str,'Message'] = None) -> 'Message':
            """Send an animation to this user"""
            return self.client.send_animation(self.id,animation,caption,parse_mode,reply_markup,reply_to_message)
    
    def send_voice(self, voice: Union[str, bytes, InputFile],
                    caption: Optional[str] = None,
                    parse_mode: Optional[str] = None,
                    reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None,reply_to_message: Union[int,str,'Message'] = None) -> 'Message':        
        """Send a voice message to this user"""
        return self.client.send_voice(self.id,voice,caption,parse_mode,reply_markup,reply_to_message)
    
    def send_media_group(self, chat_id: Union[int, str],
                            media: List[Dict],
                            reply_to_message: Union['Message', int, str] = None) -> List['Message']:
            """Send a group of photos, videos, documents or audios as an album"""
            return self.client.send_media_group(chat_id, media, reply_to_message)
        
    
    def send_location(self, latitude: float, longitude: float,
                         reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None,reply_to_message: Union[str,int,'Message'] = None) -> 'Message':
            """Send a location to this user"""
            return self.send_location(latitude,longitude,reply_markup,reply_to_message)
    
    def send_contact(self, phone_number: str, first_name: str,last_name: Optional[str] = None,reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None, reply_to_message: Union[str,int,'Message'] = None) -> 'Message':
            """Send a contact to this user"""
            return self.client.send_contact(self.id,phone_number,first_name,last_name,reply_markup,reply_to_message)
    
    def send_invoice(self,title:str,description:str,payload:str,provider_token:str,prices:list,photo_url: Optional[str] = None,reply_to_message: Union[int,str,'Message'] = None, reply_markup: Union[MenuKeyboardMarkup|InlineKeyboardMarkup] = None):
        return self.client.send_invoice(self.id,title,description,payload,provider_token,prices,photo_url,reply_to_message,reply_markup)

class Message:
    """Represents a message in Bale"""
    def __init__(self, client: 'Client', data: Dict[str, Any]):
        if not data.get('ok'):
            raise BaleException(f"API request failed: {traceback.format_exc()}")
        self.client = client
        self.ok = data.get('ok')
        result = data.get('result', {})
        
        self.message_id = self.id = result.get('message_id')
        self.from_user = self.author = User(client,{'ok': True, 'result': result.get('from', {})})
        self.date = result.get('date')
        self.chat = Chat(client, {'ok': True, 'result': result.get('chat', {})})
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
        self.forward_from = User(client, {'ok': True, 'result': result.get('forward_from', {})})
        self.forward_from_message_id = result.get('forward_from_message_id')
        self.invoice = Invoice(result.get('invoice'))
        self.reply = self.reply_message
        self.send = lambda text, parse_mode=None, reply_markup=None: self.client.send_message(self.chat.id, text, parse_mode, reply_markup, reply_to_message=self)

        

    def edit(self, text: str, parse_mode: Optional[str] = None, 
            reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
        """Edit this message"""
        return self.client.edit_message(self.chat.id, self.message_id, text, parse_mode, reply_markup)
        
    def delete(self) -> bool:
        """Delete this message"""
        return self.client.delete_message(self.chat.id, self.message_id)
        
    def reply_message(self, text: str, parse_mode: Optional[str] = None, 
                    reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
        """Send a message to this user"""
        return self.client.send_message(self.chat.id, text, parse_mode, reply_markup,reply_to_message=self)
    def reply_photo(self, photo: Union[str, bytes, InputFile],
                  caption: Optional[str] = None,
                  parse_mode: Optional[str] = None,
                  reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
        """Send a photo to a chat"""
        return self.client.send_photo(self.chat.id, photo, caption, parse_mode, reply_markup,reply_to_message=self)
    
    
    def reply_audio(self, audio: Union[str, bytes, InputFile],
                      caption: Optional[str] = None,
                      parse_mode: Optional[str] = None,
                      reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
            """Send an audio file to this user"""
            self.client.send_audio(self.chat.id, audio, caption, parse_mode, reply_markup, reply_to_message=self)
    
    def reply_document(self, document: Union[str, bytes, InputFile],
                         caption: Optional[str] = None,
                         parse_mode: Optional[str] = None,
                         reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
            """Send a document to this user"""
            self.client.send_document(self.chat.id, document, caption, parse_mode, reply_markup, reply_markup, reply_to_message=self)
    
    def reply_video(self, video: Union[str, bytes, InputFile],
                      caption: Optional[str] = None,
                      parse_mode: Optional[str] = None,
                      reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
            """Send a video to this user"""
            self.client.send_video(self.chat.id,video,caption,parse_mode,reply_markup, reply_to_message=self)
    
    def reply_animation(self, animation: Union[str, bytes, InputFile],
                          caption: Optional[str] = None,
                          parse_mode: Optional[str] = None,
                          reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
            """Send an animation to this user"""
            return self.client.send_animation(self.chat.id,animation,caption,parse_mode,reply_markup, reply_to_message=self)
    
    def reply_voice(self, voice: Union[str, bytes, InputFile],
                    caption: Optional[str] = None,
                    parse_mode: Optional[str] = None,
                    reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':        
        """Send a voice message to this user"""
        return self.client.send_voice(self.chat.id,voice,caption,parse_mode,reply_markup, reply_to_message=self)
    
    def reply_media_group(self, media: List[Dict],
                            reply_to_message: Union['Message', int, str] = None) -> List['Message']:
            """Send a group of photos, videos, documents or audios as an album"""
            return self.client.send_media_group(self.chat.id, media, reply_to_message=self)
        
    
    def reply_location(self, latitude: float, longitude: float,
                         reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> 'Message':
            """Send a location to this user"""
            return self.client.send_location(self.chat.id,latitude,longitude,reply_markup, reply_to_message=self)
    
    def reply_contact(self, phone_number: str, first_name: str,last_name: Optional[str] = None,reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None, reply_to_message: Union[str,int,'Message'] = None) -> 'Message':
            """Send a contact to this user"""
            return self.client.send_contact(self.chat.id,phone_number,first_name,last_name,reply_markup,reply_to_message)
    
    def reply_invoice(self,title:str,description:str,payload:str,provider_token:str,prices:list,photo_url: Optional[str] = None, reply_markup: Union[MenuKeyboardMarkup|InlineKeyboardMarkup] = None):
        return self.client.send_invoice(self.chat.id,title,description,payload,provider_token,prices,photo_url,self,reply_markup)

class Client:
    """Main client class for interacting with Bale API"""
    def __init__(self, token: str, session: str = 'https://tapi.bale.ai', database_name='database.db'):
        self.token = token
        self.session = session
        self.states = {}
        self.database_name = database_name
        self._base_url = f"{session}/bot{token}"
        self._session = requests.Session()
        self._message_handler = None
        self._threads = []
    
    def set_state(self, chat_or_user_id: Union[Chat,User,int,str], state: str) -> None:
        """Set the state for a chat or user"""
        if isinstance(chat_or_user_id, (Chat, User)):
            chat_or_user_id = chat_or_user_id.id
        self.states[str(chat_or_user_id)] = state
    
    def get_state(self, chat_or_user_id: Union[Chat,User,int,str]) -> str|None:
        """Get the state for a chat or user"""
        if isinstance(chat_or_user_id, (Chat, User)):
            chat_or_user_id = chat_or_user_id.id
        return self.states.get(str(chat_or_user_id))
    
    def del_state(self, chat_or_user_id: Union[Chat,User,int,str]) -> None:
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

        
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an HTTP request to Bale API"""
        url = f"{self._base_url}/{endpoint}"
        response = self._session.request(method, url, **kwargs)
        response_data = response.json()
        if not response_data.get('ok'):
            raise BaleException(response_data['error_code'], response_data['description'])
        return response_data
        
    def __del__(self):
        if hasattr(self, '_session'):
            self._session.close()
            
    def get_me(self) -> User:
        """Get information about the bot"""
        data = self._make_request('GET', 'getMe')
        return User(self, data)
        
    def get_updates(self, offset: Optional[int] = None, 
                   limit: Optional[int] = None,
                   timeout: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get latest updates/messages"""
        params = {
            'offset': offset,
            'limit': limit,
            'timeout': timeout
        }
        response = self._make_request('GET', 'getUpdates', params=params)
        return response.get('result', [])
        
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
        
    def send_message(self, chat_id: Union[int, str], text: str,
                parse_mode: Optional[str] = None,
                reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None,
                reply_to_message: Union[Message,int,str] = None) -> Message:
        """Send a message to a chat"""
        # Convert text to string if it isn't already
        text = str(text)
        
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup.keyboard if reply_markup else None,
            'reply_to_message_id': reply_to_message.message_id if isinstance(reply_to_message, Message) else reply_to_message
        }
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
        
    def send_photo(self, chat_id: Union[int, str], photo: Union[str, bytes, InputFile],
                  caption: Optional[str] = None,
                  parse_mode: Optional[str] = None,
                  reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None,
                  reply_to_message: Union[Message, int, str] = None) -> Message:
        """Send a photo to a chat"""
        files = None
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup.keyboard if reply_markup else None,
            'reply_to_message_id': reply_to_message.message_id if isinstance(reply_to_message, Message) else reply_to_message
        }
        
        if isinstance(photo, (bytes, InputFile)) or hasattr(photo, 'read'):
            files = {'photo': photo if not isinstance(photo, InputFile) else photo.file}
        else:
            data['photo'] = photo
            
        response = self._make_request('POST', 'sendPhoto', data=data, files=files)
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
        
    def edit_message(self, chat_id: Union[int, str],
                    message_id: int, text: str,
                    parse_mode: Optional[str] = None,
                    reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None) -> Message:
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
    
    def send_audio(self, chat_id: Union[int, str], audio,
                  caption: Optional[str] = None,
                  parse_mode: Optional[str] = None,
                  reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None,
                  reply_to_message: Union[Message, int, str] = None) -> Message:
        """Send an audio file"""
        files = None
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup.keyboard if reply_markup else None,
            'reply_to_message_id': reply_to_message.message_id if isinstance(reply_to_message, Message) else reply_to_message
        }
        if isinstance(audio, (bytes, InputFile)) or hasattr(audio, 'read'):
            files = {'audio': audio if not isinstance(audio, InputFile) else audio.file}
        else:
            data['audio'] = audio
                            
        response = self._make_request('POST', 'sendAudio', data=data, files=files)
        return Message(self, response)
            
    def send_document(self, chat_id: Union[int, str], document,
                        caption: Optional[str] = None,
                        parse_mode: Optional[str] = None,
                        reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None,
                        reply_to_message: Union[Message, int, str] = None) -> Message:
        """Send a document"""
        files = None
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup.keyboard if reply_markup else None,
            'reply_to_message_id': reply_to_message.message_id if isinstance(reply_to_message, Message) else reply_to_message
            }
            
        if isinstance(document, (bytes, InputFile)) or hasattr(document, 'read'):
            files = {'document': document if not isinstance(document, InputFile) else document.file}
        else:
            data['document'] = document
                
        response = self._make_request('POST', 'sendDocument', data=data, files=files)
        return Message(self, response)
            
    def send_video(self, chat_id: Union[int, str], video,
                       caption: Optional[str] = None,
                       parse_mode: Optional[str] = None,
                       reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None,
                       reply_to_message: Union[Message, int, str] = None) -> Message:
            """Send a video"""
            files = None
            data = {
                'chat_id': chat_id,
                'caption': caption,
                'parse_mode': parse_mode,
                'reply_markup': reply_markup.keyboard if reply_markup else None,
                'reply_to_message_id': reply_to_message.message_id if isinstance(reply_to_message, Message) else reply_to_message
            }
            
            if isinstance(video, (bytes, InputFile)) or hasattr(video, 'read'):
                files = {'video': video if not isinstance(video, InputFile) else video.file}
            else:
                data['video'] = video
                
            response = self._make_request('POST', 'sendVideo', data=data, files=files)
            return Message(self, response)
            
    def send_animation(self, chat_id: Union[int, str], animation,
                          caption: Optional[str] = None,
                          parse_mode: Optional[str] = None,
                          reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None,
                          reply_to_message: Union[Message, int, str] = None) -> Message:
            """Send an animation (GIF or H.264/MPEG-4 AVC video without sound)"""
            files = None
            data = {
                'chat_id': chat_id,
                'caption': caption,
                'parse_mode': parse_mode,
                'reply_markup': reply_markup.keyboard if reply_markup else None,
                'reply_to_message_id': reply_to_message.message_id if isinstance(reply_to_message, Message) else reply_to_message
            }
            
            if isinstance(animation, (bytes, InputFile)) or hasattr(animation, 'read'):
                files = {'animation': animation if not isinstance(animation, InputFile) else animation.file}
            else:
                data['animation'] = animation
                
            response = self._make_request('POST', 'sendAnimation', data=data, files=files)
            return Message(self, response)
            
    def send_voice(self, chat_id: Union[int, str], voice,
                       caption: Optional[str] = None,
                       parse_mode: Optional[str] = None,
                       reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None,
                       reply_to_message: Union[Message, int, str] = None) -> Message:
            """Send a voice message"""
            files = None
            data = {
                'chat_id': chat_id,
                'caption': caption,
                'parse_mode': parse_mode,
                'reply_markup': reply_markup.keyboard if reply_markup else None,
                'reply_to_message_id': reply_to_message.message_id if isinstance(reply_to_message, Message) else reply_to_message
            }
            
            if isinstance(voice, (bytes, InputFile)) or hasattr(voice, 'read'):
                files = {'voice': voice if not isinstance(voice, InputFile) else voice.file}
            else:
                data['voice'] = voice
                
            response = self._make_request('POST', 'sendVoice', data=data, files=files)
            return Message(self, response)
            
    def send_media_group(self, chat_id: Union[int, str],
                            media: List[Dict],
                            reply_to_message: Union[Message, int, str] = None) -> List[Message]:
            """Send a group of photos, videos, documents or audios as an album"""
            data = {
                'chat_id': chat_id,
                'media': media,
                'reply_to_message_id': reply_to_message.message_id if isinstance(reply_to_message, Message) else reply_to_message
            }
            response = self._make_request('POST', 'sendMediaGroup', json=data)
            return [Message(self, msg) for msg in response]
            
    def send_location(self, chat_id: Union[int, str],
                         latitude: float, longitude: float,
                         reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None,
                         reply_to_message: Union[Message, int, str] = None) -> Message:
            """Send a point on the map"""
            data = {
                'chat_id': chat_id,
                'latitude': latitude,
                'longitude': longitude,
                'reply_markup': reply_markup.keyboard if reply_markup else None,
                'reply_to_message_id': reply_to_message.message_id if isinstance(reply_to_message, Message) else reply_to_message
            }
            response = self._make_request('POST', 'sendLocation', json=data)
            return Message(self, response)
            
    def send_contact(self, chat_id: Union[int, str],
                        phone_number: str, first_name: str,
                        last_name: Optional[str] = None,
                        reply_markup: Union[MenuKeyboardMarkup,InlineKeyboardMarkup] = None,
                        reply_to_message: Union[Message, int, str] = None) -> Message:
            """Send a phone contact"""
            data = {
                'chat_id': chat_id,
                'phone_number': phone_number,
                'first_name': first_name,
                'last_name': last_name,
                'reply_markup': reply_markup.keyboard if reply_markup else None,
                'reply_to_message_id': reply_to_message.message_id if isinstance(reply_to_message, Message) else reply_to_message
            }
            response = self._make_request('POST', 'sendContact', json=data)
            return Message(self, response)
    
    def send_invoice(self,chat_id: Union[int,str],title:str,description:str,payload:str,provider_token:str,prices:list,photo_url: Optional[str] = None,reply_to_message: Union[int|str|Message] = None, reply_markup: Union[MenuKeyboardMarkup|InlineKeyboardMarkup] = None) -> Message:
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
            'reply_to_message_id': reply_to_message.message_id if isinstance(reply_to_message, Message) else reply_to_message,
            'reply_markup': reply_markup.keyboard if reply_markup else None
        }
        response = self._make_request('POST', 'sendInvoice', json=data)
        return Message(self, response)
    
    def copy_message(self, chat_id: Union[int,str,'Chat'], from_chat_id: Union[int,str,'Chat'], message_id: Union[int,str,'Chat']):
        data = {
            'chat_id': chat_id if isinstance(chat_id, (int, str)) else chat_id.id,
            'from_chat_id': from_chat_id if isinstance(from_chat_id, (int, str)) else from_chat_id.id,
            'message_id': message_id if isinstance(message_id, (int, str)) else message_id.id
        }
        response = self._make_request('POST', 'copyMessage', json=data)
        return Message(self, response)
    
    def get_chat_member(self, chat: Union[int,str,'Chat'], user: Union[int,str,'User']) -> ChatMember:
            """Get information about a member of a chat including their permissions"""
            data = {
                'chat_id': chat if isinstance(chat, (int, str)) else chat.id,
                'user_id': user if isinstance(user, (int, str)) else user.id
            }
            response = self._make_request('POST', 'getChatMember', json=data)
            return ChatMember(self, response['result'])

    def get_chat_administrators(self, chat: Union[int,str,'Chat']) -> List[ChatMember]:
        """Get a list of administrators in a chat"""
        data = {'chat_id': getattr(chat, 'id', chat)}
        response = self._make_request('POST', 'getChatAdministrators', json=data)
        return [ChatMember(self, member) for member in response.get('result', [])]
    
    def get_chat_members_count(self, chat: Union[int,str,'Chat']) -> int:
            """Get the number of members in a chat"""
            data = {
                'chat_id': chat if isinstance(chat, (int, str)) else chat.id
            }
            response = self._make_request('GET', 'getChatMembersCount', json=data)
            return response['result']
    
    def is_joined(self, user: Union[User,int,str], chat: Union[Chat,int,str]) -> bool:
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
            self._tick_handlers[func] = {'interval': seconds, 'last_run': 0}
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
    
    def _create_thread(self, handler, *args):
        """Helper method to create and start a thread"""
        thread = threading.Thread(target=handler, args=args, daemon=True)
        thread.start()
        self._threads.append(thread)
        
    def _handle_message(self, message, update):
        """Handle different types of messages"""
        if 'message' in update:
            msg_data = update['message']
            if 'new_chat_members' in msg_data and hasattr(self, '_member_join_handler'):
                chat = msg_data['chat']
                user = msg_data['new_chat_members'][0]
                self._create_thread(self._member_join_handler, message, Chat(self,{"ok":True,"result":chat}), User(self,{"ok":True,"result":user}))
            elif 'left_chat_member' in msg_data and hasattr(self, '_member_leave_handler'):
                chat = msg_data['chat']
                user = msg_data['left_chat_member']
                self._create_thread(self._member_leave_handler, message, Chat(self,{"ok":True,"result":chat}), User(self,{"ok":True,"result":user}))
            elif self._message_handler:
                args = (message, update) if len(inspect.signature(self._message_handler).parameters) > 1 else (message,)
                self._create_thread(self._message_handler, *args)
    
    def _handle_update(self, update):
        if hasattr(self, '_update_handler'):
            self._create_thread(self._update_handler, update)
            
        update_type = next((key for key in ('message', 'edited_message', 'callback_query') if key in update), None)
        if update_type == 'message':
            message = Message(self, {'ok': True, 'result': update['message']})
            self._handle_message(message, update)
        elif update_type == 'edited_message' and hasattr(self, '_message_edit_handler'):
            edited_message = Message(self, {'ok': True, 'result': update['edited_message']})
            args = (edited_message, update) if len(inspect.signature(self._message_edit_handler).parameters) > 1 else (edited_message,)
            self._create_thread(self._message_edit_handler, *args)
        elif update_type == 'callback_query' and self._callback_handler:
            callback_query = CallbackQuery(self, {'ok': True, 'result': update['callback_query']})
            args = (callback_query, update) if len(inspect.signature(self._callback_handler).parameters) > 1 else (callback_query,)
            self._create_thread(self._callback_handler, *args)

    def _handle_tick_events(self, current_time):
        """Handle periodic tick events"""
        if hasattr(self, '_tick_handlers'):
            for handler, info in self._tick_handlers.items():
                if current_time - info['last_run'] >= info['interval']:
                    self._create_thread(handler)
                    info['last_run'] = current_time
            
    def run(self):
        """Start polling for new messages"""
        self._polling = True
        offset = 0
        past_updates = set()
        
        if hasattr(self, '_ready_handler'):
            self._ready_handler()
            
        while self._polling:
            try:
                updates = self.get_updates(offset=offset, timeout=30)
                for update in updates:
                    update_id = update['update_id']
                    if update_id not in past_updates:
                        self._handle_update(update)
                        offset = update_id + 1
                        past_updates.add(update_id)
                        if len(past_updates) > 100:
                            past_updates.clear()
                            past_updates = set(sorted(list(past_updates))[-50:])
                
                current_time = time.time()
                self._handle_tick_events(current_time)
                self._threads = [t for t in self._threads if t.is_alive()]
                time.sleep(0.1)  # Reduced sleep time
            except Exception as e:
                print(f"Error in polling: {traceback.format_exc()}")
                time.sleep(1)
                continue

    def get_updates(self, offset: Optional[int] = None, 
                   limit: Optional[int] = None,
                   timeout: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get latest updates/messages"""
        params = {k: v for k, v in {
            'offset': offset,
            'limit': limit,
            'timeout': timeout
        }.items() if v is not None}
        response = self._make_request('GET', 'getUpdates', params=params)
        return response.get('result', [])

    def safe_close(self):
        """Close the client and stop polling"""
        self._polling = False
        for thread in self._threads:
            thread.join(timeout=1.0)
        self._threads.clear()
        if hasattr(self, '_close_handler'):
            self._close_handler()