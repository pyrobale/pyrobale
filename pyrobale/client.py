from .base import Client
from .models import (
                    DataBase, BaleException, ChatMember, CallbackQuery, 
                    Chat, User, Message, MenuKeyboardMarkup, 
                    InlineKeyboardMarkup, InputFile
)
from .exceptions import (
                    BaleAPIError, BaleAuthError, BaleException, BaleForbiddenError,
                    BaleNetworkError, BaleNotFoundError, BaleRateLimitError,
                    BaleServerError, BaleTimeoutError, BaleTokenNotFoundError,
                    BaleUnknownError, BaleValidationError
)
import requests
from typing import Union, Optional, Dict, Any, List, Tuple, Callable
import threading
import traceback
import sqlite3
import time
import sys
import collections
import inspect
import os
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