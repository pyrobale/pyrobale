from typing import Optional, Union, List, Dict, Any, Callable, Awaitable, TypeVar
from ..objects.animation import Animation
from ..objects.audio import Audio
from ..objects.callbackquery import CallbackQuery
from ..objects.chatmember import ChatMember
from ..objects.chatphoto import ChatPhoto
from ..objects.chat import Chat
from ..objects.contact import Contact
from ..objects.copytextbutton import CopyTextButton
from ..objects.document import Document
from ..objects.file import File
from ..objects.inlinekeyboardbutton import InlineKeyboardButton
from ..objects.inlinekeyboardmarkup import InlineKeyboardMarkup
from ..objects.inputfile import InputFile
from ..objects.inputmedias import InputMedia, InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo
from ..objects.invoice import Invoice
from ..objects.keyboardbutton import KeyboardButton
from ..objects.labeledprice import LabeledPrice
from ..objects.location import Location
from ..objects.messageid import MessageId
from ..objects.message import Message
from ..objects.photosize import PhotoSize
from ..objects.precheckoutquery import PreCheckoutQuery
from ..objects.replykeyboardmarkup import ReplyKeyboardMarkup
from ..objects.sticker import Sticker
from ..objects.stickerset import StickerSet
from ..objects.successfulpayment import SuccessfulPayment
from ..objects.user import User
from ..objects.video import Video
from ..objects.voice import Voice
from ..objects.webappdata import WebAppData
from ..objects.webappinfo import WebAppInfo
from ..objects.utils import *
import asyncio
import aiohttp
import bale

class Client:
    """
    A client for interacting with the Bale messenger API.
    token: The bot token to use for authentication.
    """
    def __init__(self, token: str, base_url: str = "https://tapi.bale.ai/bot"):
        self.token = token
        self.base_url = base_url
        self.requests_base =  base_url+token
        print(self.requests_base)
    
    async def get_updates(self,
                          offset: Optional[int] = None,
                          limit: Optional[int] = None,
                          timeout: Optional[int] = None) -> List[Dict]:
        data = await make_get(self.requests_base+f"/getUpdates?offset={offset}&limit={limit}&timeout={timeout}")
        return data['result']
    
    async def set_webhook(self, url: str) -> bool:
        data = await make_post(self.requests_base+"/setWebhook", data={
            "url": url
        })
        return data['result']
    
    async def get_webhook_info(self) -> Dict:
            data = await make_get(self.requests_base+"/getWebhookInfo")
            return data['result']
    

    async def get_me(self) -> User:
        data = await make_get(self.requests_base+"/getMe")
        return User(**data['result'])
    
    async def logout(self) -> bool:
        data = await make_get(self.requests_base+"/logOut")
        return data['result']
    
    async def close(self) -> bool:
        data = await make_get(self.requests_base+"/close")
        return data['result']
    
    async def send_message(self,
                           chat_id: int,
                           text: str,
                           reply_to_message_id: Optional[int] = None,
                           reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None) -> Message:
        data = await make_post(self.requests_base+"/sendMessage", data={
            "chat_id": chat_id,
            "text": text,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": reply_markup
        })
        return Message(**pythonize(data['result']))
    
    async def forward_message(self,
                              chat_id: int,
                              from_chat_id: int,
                              message_id: int) -> Message:
        data = await make_post(self.requests_base+"/forwardMessage", data={
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id})
        return Message(**pythonize(data['result']))
    
    async def copy_message(self,
                           chat_id: int,
                           from_chat_id: int,
                           message_id: int) -> Message:
        data = await make_post(self.requests_base+"/copyMessage", data={
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id})
        return Message(**pythonize(data['result']))
    
    
    async def send_photo(self,
                         chat_id: Union[int,str],
                         from_chat_id: Union[int,str],
                         photo: Union[InputFile,str],
                         caption: Optional[str] = None,
                         reply_to_message_id: Optional[int]= None,
                         reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None) -> Message:
        data = await make_post(self.requests_base+"/sendPhoto", data={
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "photo": photo,
            "caption": caption,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": reply_markup
        })
        return Message(**pythonize(data['result']))
    
    async def send_audio(self,
                         chat_id: int,
                         audio: Union[InputFile, str],
                         caption: Optional[str] = None,
                         reply_to_message_id: Optional[int] = None,
                         reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None) -> Message:
        data = await make_post(self.requests_base+"/sendAudio", data={
            "chat_id": chat_id,
            "audio": audio,
            "caption": caption,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": reply_markup
        })
        return Message(**pythonize(data['result']))
    
    async def send_document(self,
                            chat_id: int,
                            document: Union[InputFile, str],
                            caption: Optional[str] = None,
                            reply_to_message_id: Optional[int] = None,
                            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None) -> Message:
        data = await make_post(self.requests_base+"/sendDocument", data={
            "chat_id": chat_id,
            "document": document,
            "caption": caption,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": reply_markup
        })
        return Message(**pythonize(data['result']))
    
    async def send_video(self,
                         chat_id: int,
                         video: Union[InputFile, str],
                         caption: Optional[str] = None,
                         reply_to_message_id: Optional[int] = None,
                         reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None) -> Message:
        data = await make_post(self.requests_base+"/sendVideo", data={
            "chat_id": chat_id,
            "video": video,
            "caption": caption,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": reply_markup
        })
        return Message(**pythonize(data['result']))
    
    async def send_animation(self,
                             chat_id: int,
                             animation: Union[InputFile, str],
                             caption: Optional[str] = None,
                             reply_to_message_id: Optional[int] = None,
                             reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None) -> Message:
        data = await make_post(self.requests_base+"/sendAnimation", data={
            "chat_id": chat_id,
            "animation": animation,
            "caption": caption,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": reply_markup
        })
        return Message(**pythonize(data['result']))
    
    async def send_voice(self,
                         chat_id: int,
                         voice: Union[InputFile, str],
                         caption: Optional[str] = None,
                         reply_to_message_id: Optional[int] = None,
                         reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None) -> Message:
        data = await make_post(self.requests_base+"/sendVoice", data={
            "chat_id": chat_id,
            "voice": voice,
            "caption": caption,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": reply_markup
        })
        return Message(**pythonize(data['result']))
    
    async def send_media_group(self,
                               chat_id: int,
                               media: List[Union[InputMediaPhoto, InputMediaVideo, InputMediaAudio]],
                               reply_to_message_id: Optional[int] = None,
                               reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None) -> Message:
        data = await make_post(self.requests_base+"/sendMediaGroup", data={
            "chat_id": chat_id,
            "media": media,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": reply_markup
        })
        return Message(**pythonize(data['result']))
    
    async def send_location(self,
                            chat_id: int,
                            latitude: float,
                            longitude: float,
                            reply_to_message_id: Optional[int] = None,
                            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None) -> Message:
        data = await make_post(self.requests_base+"/sendLocation", data={
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": reply_markup
        })
        return Message(**pythonize(data['result']))
    
    async def send_contact(self,
                           chat_id: int,
                           phone_number: str,
                           first_name: str,
                           last_name: Optional[str] = None,
                           reply_to_message_id: Optional[int] = None,
                           reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None) -> Message:
        data = await make_post(self.requests_base+"/sendContact", data={
            "chat_id": chat_id,
            "phone_number": phone_number,
            "first_name": first_name,
            "last_name": last_name,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": reply_markup
        })
        return Message(**pythonize(data['result']))
    
    async def get_file(self, file_id: str) -> File:
        data = await make_post(self.requests_base+"/getFile", data={
            "file_id": file_id
        })
        return File(**pythonize(data['result']))
    
    async def ban_chat_member(self,
                              chat_id: int,
                              user_id: int) -> bool:
        data = await make_post(self.requests_base+"/banChatMember", data={
            "chat_id": chat_id,
            "user_id": user_id
        })
        return data.get("ok", False)
    
    async def unban_chat_member(self,
                                chat_id: int,
                                user_id: int) -> bool:
        data = await make_post(self.requests_base+"/unbanChatMember", data={
            "chat_id": chat_id,
            "user_id": user_id
        })
        return data.get("ok", False)
    
    async def promote_chat_member(self,
                                  chat_id: int,
                                  user_id: int,
                                  can_change_info: Optional[bool] = None,
                                  can_post_messages: Optional[bool] = None,
                                  can_edit_messages: Optional[bool] = None,
                                  can_delete_messages: Optional[bool] = None,
                                  can_invite_users: Optional[bool] = None,
                                  can_restrict_members: Optional[bool] = None,
                                  can_pin_messages: Optional[bool] = None,
                                  can_promote_members: Optional[bool] = None):
        data = await make_post(self.requests_base+"/promoteChatMember", data={
            "chat_id": chat_id,
            "user_id": user_id,
            "can_change_info": can_change_info,
            "can_post_messages": can_post_messages,
            "can_edit_messages": can_edit_messages,
            "can_delete_messages": can_delete_messages,
            "can_invite_users": can_invite_users,
            "can_restrict_members": can_restrict_members,
            "can_pin_messages": can_pin_messages,
            "can_promote_members": can_promote_members
        })
        return data.get("ok", False)
    
    async def set_chat_photo(self,
                             chat_id: int,
                             photo: InputFile) -> bool:
        data = await make_post(self.requests_base+"/setChatPhoto", data={
            "chat_id": chat_id,
            "photo": photo
        })
        return data.get("ok", False)
    
    async def leave_chat(self,
                         chat_id: int) -> bool:
        data = await make_post(self.requests_base+"/leaveChat", data={
            "chat_id": chat_id
        })
        return data.get("ok", False)
    
    async def get_chat(self, chat_id: int) -> Chat:
        data = await make_post(self.requests_base+"/getChat", data={
            "chat_id": chat_id
        })
        return Chat(**pythonize(data['result']))
    
    async def get_chat_members_count(self, chat_id: int) -> int:
        data = await make_post(self.requests_base+"/getChatMembersCount", data={
            "chat_id": chat_id
        })
        return data.get("result", 0)
    
    async def pin_chat_message(self,
                               chat_id: int,
                               message_id: int)-> bool:
        data = await make_post(self.requests_base+"/pinChatMessage", data={
            "chat_id": chat_id,
            "message_id": message_id
        })
        return data.get("ok", False)
    
    async def unpin_chat_message(self,
                                 chat_id: int) -> bool:
        data = await make_post(self.requests_base+"/unpinChatMessage", data={
            "chat_id": chat_id
        })
        return data.get("ok", False)
    
    async def unpin_all_chat_messages(self,
                                      chat_id: int) -> bool:
        data = await make_post(self.requests_base+"/unpinAllChatMessages", data={
            "chat_id": chat_id
        })
        return data.get("ok", False)
    
    async def set_chat_title(self,
                             chat_id: int,
                             title: str) -> bool:
        data = await make_post(self.requests_base+"/setChatTitle", data={
            "chat_id": chat_id,
            "title": title
        })
        return data.get("ok", False)
    
    async def set_chat_description(self,
                                   chat_id: int,
                                   description: str) -> bool:
        data = await make_post(self.requests_base+"/setChatDescription", data={
            "chat_id": chat_id,
            "description": description
        })
        return data.get("ok", False)
    
    async def delete_chat_photo(self,
                                chat_id: int) -> bool:
        data = await make_post(self.requests_base+"/deleteChatPhoto", data={
            "chat_id": chat_id
        })
        return data.get("ok", False)
    
    async def create_chat_invite_link(self,
                                      chat_id: int) -> str:
        data = await make_post(self.requests_base+"/createChatInviteLink", data={
            "chat_id": chat_id
        })
        return data.get("result", "")
    
    async def revoke_chat_invite_link(self,
                                      chat_id: int,
                                      invite_link: str) -> str:
        data = await make_post(self.requests_base+"/revokeChatInviteLink", data={
            "chat_id": chat_id,
            "invite_link": invite_link
        })
        return data.get("result", "")
    
    async def export_chat_invite_link(self,
                                      chat_id: int) -> str:
        data = await make_post(self.requests_base+"/exportChatInviteLink", data={
            "chat_id": chat_id
        })
        return data.get("result", "")