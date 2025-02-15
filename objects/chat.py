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

    def banChatMember(
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

    def unbanChatMember(
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

    def promoteChatMember(
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

    def setChatPhoto(self, photo: Union[str, bytes, InputFile]) -> bool:
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
        response = self.client._make_request(
            'POST', 'getChatMembersCount', data=data)
        return response.get('result', 0)

    def pinChatMessage(
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

    def unPinChatMessage(self, message_id: int) -> bool:
        """Unpin a message in the chat"""
        data = {
            'chat_id': self.id,
            'message_id': message_id
        }
        response = self.client._make_request(
            'POST', 'unpinChatMessage', data=data)
        return response.get('ok', False)

    def unpinAllChatMessages(self) -> bool:
        """Unpin all messages in the chat"""
        data = {'chat_id': self.id}
        response = self.client._make_request(
            'POST', 'unpinAllChatMessages', data=data)
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
        response = self.client._make_request(
            'POST', 'setChatDescription', data=data)
        return response.get('ok', False)

    def deleteChatPhoto(self) -> bool:
        """Delete the chat photo"""
        data = {'chat_id': self.id}
        response = self.client._make_request(
            'POST', 'deleteChatPhoto', data=data)
        return response.get('ok', False)

    def createChatInviteLink(self) -> str:
        """Create an invite link for the chat"""
        data = {'chat_id': self.id}
        response = self.client._make_request(
            'POST', 'createChatInviteLink', data=data)
        return response.get('result', {}).get('invite_link')

    def revokeChatInviteLink(self, invite_link: str) -> bool:
        """Revoke an invite link for the chat"""
        data = {
            'chat_id': self.id,
            'invite_link': invite_link
        }
        response = self.client._make_request(
            'POST', 'revokeChatInviteLink', data=data)
        return response.get('ok', False)

    def exportChatInviteLink(self) -> str:
        """Generate a new invite link for the chat"""
        data = {'chat_id': self.id}
        response = self.client._make_request(
            'POST', 'exportChatInviteLink', data=data)
        return response.get('result')