from typing import TYPE_CHECKING
from typing import Optional, Union
if TYPE_CHECKING:
    from .utils import build_api_url
    from ..objects.user import User
    from ..objects.chat import Chat
    from ..objects.chatphoto import ChatPhoto
    from ..objects.animation import Animation
    from ..objects.audio import Audio
    from ..objects.document import Document
    from ..objects.photosize import PhotoSize
    from ..objects.sticker import Sticker
    from ..objects.video import Video
    from ..objects.voice import Voice
    from ..objects.contact import Contact
    from ..objects.location import Location
    from ..objects.invoice import Invoice
    from ..objects.successfulpayment import SuccessfulPayment
    from ..objects.webappdata import WebAppData
    from ..objects.webappinfo import WebAppInfo
    from ..objects.inlinekeyboardmarkup import InlineKeyboardMarkup
    from ..objects.replykeyboardmarkup import ReplyKeyboardMarkup
    from ..client import Client
from ..objects.chat import Chat
from ..objects.user import User
import asyncio
import aiohttp


class Message:
    def __init__(self,
                 message_id: Optional[int] = None,
                 from_user: Optional['User'] = None,
                 date: Optional[int] = None,
                 chat: Optional['Chat'] = None,
                 text: Optional[str] = None,
                 forward_from: Optional['User'] = None,
                 forward_from_chat: Optional['Chat'] = None,
                 forward_from_message_id: Optional[int] = None,
                 forward_date: Optional[int] = None,
                 edite_date: Optional[int] = None,
                 animation: Optional['Animation'] = None,
                 audio: Optional['Audio'] = None,
                 document: Optional['Document'] = None,
                 photo: Optional[list['PhotoSize']] = None,
                 sticker: Optional['Sticker'] = None,
                 video: Optional['Video'] = None,
                 voice: Optional['Voice'] = None,
                 caption: Optional[str] = None,
                 contact: Optional['Contact'] = None,
                 location: Optional['Location'] = None,
                 new_chat_members: Optional[list['User']] = None,
                 left_chat_member: Optional['User'] = None,
                 invoice: Optional['Invoice'] = None,
                 successful_payment: Optional['SuccessfulPayment'] = None,
                 web_app_data: Optional['WebAppData'] = None,
                 reply_markup: Optional['InlineKeyboardMarkup'] = None,
                 **kwargs
                 ):
        self.id: int = message_id
        self.user: 'User' = User(**from_user) if from_user else None
        self.date: int = date
        self.chat: Optional['Chat'] = chat if isinstance(chat, Chat) else Chat(**chat) if chat else None
        self.forward_from: Optional['User'] = forward_from
        self.forward_from_chat: Optional['Chat'] = forward_from_chat
        self.forward_from_message_id: Optional[int] = forward_from_message_id
        self.forward_date: Optional[int] = forward_date
        self.edite_date: Optional[int] = edite_date
        self.text: Optional[str] = text
        self.animation: Optional['Animation'] = animation
        self.audio: Optional['Audio'] = audio
        self.document: Optional['Document'] = document
        self.photo: Optional[list['PhotoSize']] = photo
        self.sticker: Optional['Sticker'] = sticker
        self.video: Optional['Video'] = video
        self.voice: Optional['Voice'] = voice
        self.caption: Optional[str] = caption
        self.contact: Optional['Contact'] = contact
        self.location: Optional['Location'] = location
        self.new_chat_members: Optional[list['User']] = new_chat_members
        self.left_chat_member: Optional['User'] = left_chat_member
        self.invoice: Optional['Invoice'] = invoice
        self.successful_payment: Optional['SuccessfulPayment'] = successful_payment
        self.web_app_data: Optional['WebAppData'] = web_app_data
        self.reply_markup: Optional['InlineKeyboardMarkup'] = reply_markup
        self.client : Client = kwargs.get('kwargs',{}).get('client')
        
        
    async def reply(self, text: str, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None):
        if self.chat and self.chat.id:
            await self.client.send_message(self.chat.id, text, reply_markup=reply_markup)
    
    async def edit(self, text: str, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None):
        if self.chat and self.chat.id and self.id:
            await self.client.edit_message(self.chat.id, self.id, text, reply_markup=reply_markup)
    
    async def delete(self):
        if self.chat and self.chat.id and self.id:
            await self.client.delete(self.chat.id, self.id)

    async def forward(self, chat_id: int):
        if self.chat and self.chat.id and self.id:
            await self.client.forward(self.chat.id, chat_id, self.id)

    async def reply_photo(self, photo: str, caption: Optional[str] = None, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None):
        if self.chat and self.chat.id:
            await self.client.send_photo(self.chat.id, photo=photo, caption=caption, reply_markup=reply_markup)
    
    async def reply_video(self, video: str, caption: Optional[str] = None, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None):
        if self.chat and self.chat.id:
            await self.client.send_video(self.chat.id, video=video, caption=caption, reply_markup=reply_markup)

    async def reply_audio(self, audio: str, caption: Optional[str] = None, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None):
        if self.chat and self.chat.id:
            await self.client.send_audio(self.chat.id, audio=audio, caption=caption, reply_markup=reply_markup)

    async def reply_document(self, document: str, caption: Optional[str] = None, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None):
        if self.chat and self.chat.id:
            await self.client.send_document(self.chat.id, document=document, caption=caption, reply_markup=reply_markup)

    async def reply_sticker(self, sticker: str, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None):
        if self.chat and self.chat.id:
            await self.client.send_sticker(self.chat.id, sticker=sticker, reply_markup=reply_markup)

    async def reply_location(self, latitude: float, longitude: float, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None):
        if self.chat and self.chat.id:
            await self.client.send_location(self.chat.id, latitude=latitude, longitude=longitude, reply_markup=reply_markup)

    async def reply_contact(self, phone_number: str, first_name: str, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None):
        if self.chat and self.chat.id:
            await self.client.send_contact(self.chat.id, phone_number=phone_number, first_name=first_name, reply_markup=reply_markup)

    async def reply_invoice(self, title: str, description: str, payload: str, provider_token: str, currency: str, prices: list, reply_markup: Union['ReplyKeyboardMarkup','InlineKeyboardMarkup'] = None):
        if self.chat and self.chat.id:
            await self.client.send_invoice(self.chat.id, title=title, description=description, payload=payload, provider_token=provider_token, currency=currency, prices=prices, reply_markup=reply_markup)
    