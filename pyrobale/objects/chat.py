from typing import TYPE_CHECKING
from typing import Optional,Union
if TYPE_CHECKING:
    from .utils import build_api_url
    from .chatphoto import ChatPhoto
    from .message import Message
    from .user import User
    from .chatmember import ChatMember
    from ..client import Client
    from ..objects.inlinekeyboardmarkup import InlineKeyboardMarkup
    from ..objects.replykeyboardmarkup import ReplyKeyboardMarkup
from .enums import ChatType, ChatAction, UpdatesTypes
import asyncio
import aiohttp

class Chat:
    """
    Represents a chat in the Bale messenger.
    """
    def __init__(self,
                 id: Optional[int] = None,
                 type: Optional[str] = None,
                 title: Optional[str] = None,
                 username: Optional[str] = None,
                 first_name: Optional[str] = None,
                 last_name: Optional[str] = None,
                 photo: Optional['ChatPhoto'] = None,
                 **kwargs):
        self.id = id
        self.type = type
        self.PRIVATE = self.type == 'private'
        self.GROUP = self.type == 'group'
        self.CHANNEL = self.type == 'channel'
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.photo : 'ChatPhoto' = photo
        self.client : 'Client' = kwargs.get('kwargs',{}).get('client')
    
    async def send_message(self, text: str, reply_to_message_id: int = None, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None) -> 'Message':
        """
        Send a message to the chat.
        """
        self.client.send_message(chat_id=self.id, text=text, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)
    
    async def get_chat_member(self, user_id: int) -> 'ChatMember':
        """
        Get a chat member.
        """
        return await self.client.get_chat_member(chat_id=self.id, user_id=user_id)
    async def get_chat_members_count(self) -> int:
        """
        Get the number of members in the chat.
        """
        return await self.client.get_chat_members_count(chat_id=self.id)
    
    async def send_photo(self, photo: str, caption: Optional[str] = None, reply_to_message_id: int = None, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None) -> 'Message':
        """
        Send a photo to the chat.
        """
        self.client.send_photo(chat_id=self.id, photo=photo, caption=caption, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)
    
    async def send_video(self, video: str, caption: Optional[str] = None, reply_to_message_id: int = None, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None) -> 'Message':
        """
        Send a video to the chat.
        """
        self.client.send_video(chat_id=self.id, video=video, caption=caption, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)
    
    async def send_audio(self, audio: str, caption: Optional[str] = None, reply_to_message_id: int = None, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None) -> 'Message':
        """
        Send an audio to the chat.
        """
        self.client.send_audio(chat_id=self.id, audio=audio, caption=caption, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)
    
    async def send_document(self, document: str, caption: Optional[str] = None, reply_to_message_id: int = None, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None) -> 'Message':
        """
        Send a document to the chat.
        """
        self.client.send_document(chat_id=self.id, document=document, caption=caption, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)
    
    async def send_sticker(self, sticker: str, reply_to_message_id: int = None, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None) -> 'Message':
        """
        Send a sticker to the chat.
        """
        self.client.send_sticker(chat_id=self.id, sticker=sticker, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)
    
    async def send_voice(self, voice: str, caption: Optional[str] = None, reply_to_message_id: int = None, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None) -> 'Message':
        """
        Send a voice to the chat.
        """
        self.client.send_voice(chat_id=self.id, voice=voice, caption=caption, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)
    
    async def send_location(self, latitude: float, longitude: float, reply_to_message_id: int = None, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None) -> 'Message':
        """
        Send a location to the chat.
        """
        self.client.send_location(chat_id=self.id, latitude=latitude, longitude=longitude, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)

    async def send_contact(self, phone_number: str, first_name: str, last_name: Optional[str] = None, reply_to_message_id: int = None, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None) -> 'Message':
        """
        Send a contact to the chat.
        """
        self.client.send_contact(chat_id=self.id, phone_number=phone_number, first_name=first_name, last_name=last_name, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)
    
    async def ban(self, user_id: int, until_date: Optional[int] = None) -> bool:
        """
        Ban a user from the chat.
        """
        return await self.client.ban_chat_member(chat_id=self.id, user_id=user_id, until_date=until_date)
    
    async def unban(self, user_id: int) -> bool:
        """
        Unban a user from the chat.
        """
        return await self.client.unban_chat_member(chat_id=self.id, user_id=user_id)
    
    async def promote(self,
                      user_id: int,
                      can_change_info: Optional[bool] = None,
                      can_post_messages: Optional[bool] = None,
                      can_edit_messages: Optional[bool] = None,
                      can_delete_messages: Optional[bool] = None,
                      can_invite_users: Optional[bool] = None,
                      can_restrict_members: Optional[bool] = None,
                      can_pin_messages: Optional[bool] = None,
                      can_promote_members: Optional[bool] = None
                      ):
        """
        Promote a user in the chat.
        """
        return await self.client.promote_chat_member(chat_id=self.id, user_id=user_id, can_change_info=can_change_info, can_post_messages=can_post_messages, can_edit_messages=can_edit_messages, can_delete_messages=can_delete_messages, can_invite_users=can_invite_users, can_restrict_members=can_restrict_members, can_pin_messages=can_pin_messages, can_promote_members=can_promote_members)
    
    async def leave(self) -> bool:
        """
        Leave the chat.
        """
        return await self.client.leave_chat(chat_id=self.id)
    
    async def pin(self, message_id: int) -> bool:
        """
        Pin a message in the chat.
        """
        return await self.client.pin_chat_message(chat_id=self.id, message_id=message_id)
    
    async def unpin(self) -> bool:
        """
        Unpin a message in the chat.
        """
        return await self.client.unpin_chat_message(chat_id=self.id)
    
    async def unpin_all(self) -> bool:
        """
        Unpin all messages in the chat.
        """
        return await self.client.unpin_all_chat_messages(chat_id=self.id)
    
    async def set_title(self, title: str) -> bool:
        """
        Set the title of the chat.
        """
        return await self.client.set_chat_title(chat_id=self.id, title=title)
    
    async def set_description(self, description: str) -> bool:
        """
        Set the description of the chat.
        """
        return await self.client.set_chat_description(chat_id=self.id, description=description)
    
    async def set_photo(self, photo: str) -> bool:
        """
        Set the photo of the chat.
        """
        return await self.client.set_chat_photo(chat_id=self.id, photo=photo)

    async def send_action(self, action: ChatAction) -> bool:
        """
        Send an action to the chat.
        """
        return await self.client.send_chat_action(chat_id=self.id, action=action)