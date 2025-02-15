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
from ..objects.inputfile import(InputFile)
from ..objects.labeledprice import (LabeledPrice)
from ..objects.invoice import (Invoice)
from ..objects.chatmember import (ChatMember)

class Client:
    """Main client class for interacting with Bale API"""

    def __init__(
            self,
            token: str,
            session: str = 'https://tapi.bale.ai',
            database_name='database.db'):
        self.token = token
        self.session = session
        self.states = {}
        self.database_name = database_name
        self._base_url = f"{session}/bot{token}"
        self._session = requests.Session()
        self._message_handler = None
        self._threads = []

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
        # Convert text to string if it isn't already
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
            if 'new_chat_members' in msg_data and hasattr(
                    self, '_member_join_handler'):
                chat = msg_data['chat']
                user = msg_data['new_chat_members'][0]
                self._create_thread(
                    self._member_join_handler, message, Chat(
                        self, {
                            "ok": True, "result": chat}), User(
                        self, {
                            "ok": True, "result": user}))
            elif 'left_chat_member' in msg_data and hasattr(self, '_member_leave_handler'):
                chat = msg_data['chat']
                user = msg_data['left_chat_member']
                self._create_thread(
                    self._member_leave_handler, message, Chat(
                        self, {
                            "ok": True, "result": chat}), User(
                        self, {
                            "ok": True, "result": user}))
            elif self._message_handler:
                args = (
                    message,
                    update) if len(
                    inspect.signature(
                        self._message_handler).parameters) > 1 else (
                    message,
                )
                self._create_thread(self._message_handler, *args)

    def _handle_update(self, update):
        if hasattr(self, '_update_handler'):
            self._create_thread(self._update_handler, update)

        update_type = next(
            (key for key in (
                'message',
                'edited_message',
                'callback_query') if key in update),
            None)
        if update_type == 'message':
            message = Message(self, {'ok': True, 'result': update['message']})
            self._handle_message(message, update)
        elif update_type == 'edited_message' and hasattr(self, '_message_edit_handler'):
            edited_message = Message(
                self, {'ok': True, 'result': update['edited_message']})
            args = (
                edited_message,
                update) if len(
                inspect.signature(
                    self._message_edit_handler).parameters) > 1 else (
                edited_message,
            )
            self._create_thread(self._message_edit_handler, *args)
        elif update_type == 'callback_query' and self._callback_handler:
            callback_query = CallbackQuery(
                self, {'ok': True, 'result': update['callback_query']})
            args = (
                callback_query,
                update) if len(
                inspect.signature(
                    self._callback_handler).parameters) > 1 else (
                callback_query,
            )
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
                            past_updates = set(
                                sorted(list(past_updates))[-50:])

                current_time = time.time()
                self._handle_tick_events(current_time)
                self._threads = [t for t in self._threads if t.is_alive()]
                time.sleep(0.1)  # Reduced sleep time
            except Exception:
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