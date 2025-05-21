from typing import TYPE_CHECKING
from typing import Optional
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
    from ..objects.inlinekeyboardbutton import InlineKeyboardButton
    from ..objects.replykeyboardmarkup import ReplyKeyboardMarkup
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
                 reply_markup: Optional['InlineKeyboardButton'] = None

                 ):
        self.id = message_id
        self.user = from_user
        self.date = date
        self.chat = chat
        self.forward_from = forward_from
        self.forward_from_chat = forward_from_chat
        self.forward_from_message_id = forward_from_message_id
        self.forward_date = forward_date
        self.edite_date = edite_date
        self.text = text
        self.animation = animation
        self.audio = audio
        self.document = document
        self.photo = photo
        self.sticker = sticker
        self.video = video
        self.voice = voice
        self.caption = caption
        self.contact = contact
        self.location = location
        self.new_chat_members = new_chat_members
        self.left_chat_member = left_chat_member
        self.invoice = invoice
        self.successful_payment = successful_payment
        self.web_app_data = web_app_data
        self.reply_markup = reply_markup
