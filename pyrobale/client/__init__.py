from typing import Optional, Union, List, Dict, Any, Callable, Awaitable
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
from ..objects.inputmedias import (
    InputMedia,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
)
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
from ..objects.enums import UpdatesTypes, ChatAction, ChatType, ChatPermissions
from ..objects.peerdata import PeerData
from ..filters import Filters
from ..StateMachine import StateMachine
from ..exceptions import NotFoundException, InvalidTokenException, PyroBaleException

from enum import Enum
import asyncio
from bs4 import BeautifulSoup
from json import loads, JSONDecodeError
import aiohttp


class Client:
    """A client for interacting with the Bale messenger API.

    Args:
        token (str): The bot token.
        base_url (str, optional): The base URL for the API. Defaults to "https://tapi.bale.ai/bot".

    Returns:
        Client: The client instance.
    """

    def __init__(self, token: str, base_url: str = "https://tapi.bale.ai/bot"):
        self.token = token
        self.base_url = base_url
        self.requests_base = base_url + token

        self.handlers = []
        self._waiters = []
        self.running = False
        self.last_update_id = 0
        self.state_machine = StateMachine()

        self.check_defined_message = True
        self.defined_messages = {}

    async def get_updates(
            self,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            timeout: Optional[int] = None,
    ) -> List[Dict]:
        """Get updates from the Bale API.

        Args:
            offset (int, optional): The offset to start with. Defaults to None.
            limit (int, optional): The maximum number of updates to return. Defaults to None.
            timeout (int, optional): The maximum number of seconds to wait. Defaults to None.

        Returns:
            List[Dict]: The updates.
        """
        data = await make_get(
            self.requests_base + f"/getUpdates?offset={offset}&limit={limit}&timeout={timeout}"
        )
        if data['ok']:
            if 'result' in data:
                return data["result"]
            else:
                if data.get('error_code') == 403:
                    raise InvalidTokenException("Forbidden 403 : --ENTERED TOKEN IS NOT VALID--")
        return []

    async def set_webhook(self, url: str) -> bool:
        """Set the webhook for the bot.

        Args:
            url (str): The webhook URL.

        Returns:
            bool: True if the webhook was set.
        """
        data = await make_post(self.requests_base + "/setWebhook", data={"url": url})
        return data.get("ok", False)

    async def get_webhook_info(self) -> Dict:
        """Get the webhook information for the bot.

        Returns:
            Dict: The webhook information.
        """
        data = await make_get(self.requests_base + "/getWebhookInfo")
        return data.get("result", {})

    async def get_me(self) -> User:
        """Get information about the bot.

        Returns:
            User: The bot.
        """
        data = await make_get(self.requests_base + "/getMe")
        return User(**data["result"])

    async def logout(self) -> bool:
        """Log out the bot.

        Returns:
            bool: True if the bot was logged out.
        """
        data = await make_get(self.requests_base + "/logOut")
        return data.get("ok", False)

    async def close(self) -> bool:
        """Close the bot.

        Returns:
            bool: True if the bot was closed.
        """
        data = await make_get(self.requests_base + "/close")
        return data.get("ok", False)

    async def send_message(
            self,
            chat_id: int,
            text: str,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
    ) -> Message:
        """Send a message to a chat.

        Args:
            chat_id (int): The chat to send the message to.
            text (str): The text to send.
            reply_to_message_id (int, optional): The message ID to reply to. Defaults to None.
            reply_markup (Union[InlineKeyboardMarkup, ReplyKeyboardMarkup], optional):  The reply keyboard markup (buttons). Defaults to None.

        Returns:
            Message: The message.
        """
        data = await make_post(
            self.requests_base + "/sendMessage",
            data={
                "chat_id": chat_id,
                "text": text,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": reply_markup.to_dict() if reply_markup else None,
            },
        )
        return Message(**pythonize(data.get("result")))
        
    async def delete_message(
            self,
            chat_id: int,
            message_id: int
    ) -> bool:
        """Deletes a message from a chat.

        Args:
            chat_id (int): The chat to send the message to.
            message_id (int): The message ID to delete.

        Returns:
            bool: True if the message was deleted.
        """
        data = await make_post(
            self.requests_base + "/deleteMessage",
            data={
                "chat_id": chat_id,
                "message_id": message_id,
            },
        )
        return True

    async def forward_message(
            self, chat_id: int, from_chat_id: int, message_id: int
    ) -> Message:
        """Forward a message to a chat.

        Args:
            chat_id (int): The chat to send the message to.
            from_chat_id (int): The chat to send the message to.
            message_id (int): The message ID to forward.

        Returns:
            Message: The message.
        """
        data = await make_post(
            self.requests_base + "/forwardMessage",
            data={
                "chat_id": chat_id,
                "from_chat_id": from_chat_id,
                "message_id": message_id,
            },
        )
        return Message(**pythonize(data["result"]))

    async def copy_message(
            self, chat_id: int, from_chat_id: int, message_id: int
    ) -> Message:
        """Copy a message to a chat without forwarding.

        Args:
            chat_id (int): The chat to send the message to.
            from_chat_id (int): The chat to send the message to.
            message_id (int): The message ID to forward.

        Returns:
            Message: The message.
        """
        data = await make_post(
            self.requests_base + "/copyMessage",
            data={
                "chat_id": chat_id,
                "from_chat_id": from_chat_id,
                "message_id": message_id,
            },
        )
        return Message(**pythonize(data["result"]))

    async def send_photo(
            self,
            chat_id: Union[int, str],
            photo: Union[InputFile, str],
            caption: Optional[str] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
    ) -> Message:
        """Send a photo to a chat.

        Args:
            chat_id (Union[int, str]): The chat to send the message to.
            photo (Union[InputFile, str]): The photo to send.
            caption (Optional[str], optional): The caption of the photo. Defaults to None.
            reply_to_message_id (Optional[int], optional): The message ID to reply to. Defaults to None.
            reply_markup (Optional[InlineKeyboardMarkup], optional): The reply keyboard markup (buttons). Defaults to None.
        """
        data = await make_post(
            self.requests_base + "/sendPhoto",
            data={
                "chat_id": chat_id,
                "photo": photo,
                "caption": caption,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": reply_markup.to_dict() if reply_markup else None,
            },
        )
        return Message(**pythonize(data["result"]))

    async def send_audio(
            self,
            chat_id: int,
            audio: Union[InputFile, str],
            caption: Optional[str] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
    ) -> Message:
        """Send an audio to a chat.

        Args:
            chat_id (int): The chat to send the message to.
            audio (Union[InputFile, str]): The audio file to send.
            caption (Optional[str], optional): The caption of the audio. Defaults to None.
            reply_to_message_id (Optional[int], optional): The message ID to reply to. Defaults to None.
            reply_markup Optional[InlineKeyboardMarkup], optional): The reply keyboard markup (buttons).

        Returns:
            Message: The message.
        """
        data = await make_post(
            self.requests_base + "/sendAudio",
            data={
                "chat_id": chat_id,
                "audio": audio,
                "caption": caption,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": reply_markup.to_dict() if reply_markup else None,
            },
        )
        return Message(**pythonize(data["result"]))

    async def send_document(
            self,
            chat_id: int,
            document: Union[InputFile, str],
            caption: Optional[str] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
    ) -> Message:
        """Send a document to a chat.

        Args:
            chat_id (int): The chat to send the message to.
            document (Union[InputFile, str]): The document to send.
            caption (Optional[str], optional): The caption of the document. Defaults to None.
            reply_to_message_id (Optional[int], optional): The message ID to reply to. Defaults to None.
            reply_markup Optional[InlineKeyboardMarkup], optional): The reply keyboard markup (buttons).

        Returns:
            Message: The message.
        """
        data = await make_post(
            self.requests_base + "/sendDocument",
            data={
                "chat_id": chat_id,
                "document": document,
                "caption": caption,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": reply_markup.to_dict() if reply_markup else None,
            },
        )
        return Message(**pythonize(data["result"]))

    async def send_video(
            self,
            chat_id: int,
            video: Union[InputFile, str],
            caption: Optional[str] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
    ) -> Message:
        """Send a video to a chat.

        Args:
            chat_id (int): The chat to send the message to.
            video (Union[InputFile, str]): The video file to send.
            caption (Optional[str], optional): The caption of the video. Defaults to None.
            reply_to_message_id (Optional[int], optional): The message ID to reply to. Defaults to None.
            reply_markup Optional[InlineKeyboardMarkup], optional): The reply keyboard markup (buttons).

        Returns:
            Message: The message.
        """
        data = await make_post(
            self.requests_base + "/sendVideo",
            data={
                "chat_id": chat_id,
                "video": video,
                "caption": caption,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": reply_markup.to_dict() if reply_markup else None,
            },
        )
        return Message(**pythonize(data["result"]))

    async def send_animation(
            self,
            chat_id: int,
            animation: Union[InputFile, str],
            caption: Optional[str] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
    ) -> Message:
        """Send an animation (GIF) to a chat.

        Args:
            chat_id (int): The chat to send the message to.
            animation (Union[InputFile, str]): The animation file to send.
            caption (Optional[str], optional): The caption of the animation. Defaults to None.
            reply_to_message_id (Optional[int], optional): The message ID to reply to. Defaults to None.
            reply_markup Optional[InlineKeyboardMarkup], optional): The reply keyboard markup (buttons).

        Returns:
            Message: The message.
        """
        data = await make_post(
            self.requests_base + "/sendAnimation",
            data={
                "chat_id": chat_id,
                "animation": animation,
                "caption": caption,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": reply_markup.to_dict() if reply_markup else None,
            },
        )
        return Message(**pythonize(data["result"]))

    async def send_voice(
            self,
            chat_id: int,
            voice: Union[InputFile, str],
            caption: Optional[str] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
    ) -> Message:
        """Send a voice message to a chat.

        Args:
            chat_id (int): The chat to send the message to.
            voice (Union[InputFile, str]): The voice file to send.
            caption (Optional[str], optional): The caption of the voice. Defaults to None.
            reply_to_message_id (Optional[int], optional): The message ID to reply to. Defaults to None.
            reply_markup Optional[InlineKeyboardMarkup], optional): The reply keyboard markup (buttons).

        Returns:
            Message: The message.
        """
        data = await make_post(
            self.requests_base + "/sendVoice",
            data={
                "chat_id": chat_id,
                "voice": voice,
                "caption": caption,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": reply_markup.to_dict() if reply_markup else None,
            },
        )
        return Message(**pythonize(data["result"]))

    async def send_media_group(
            self,
            chat_id: int,
            media: List[Union[InputMediaPhoto, InputMediaVideo, InputMediaAudio]],
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
    ) -> List[Message]:
        """Send a media group to a chat.

        Args:
            chat_id (int): The chat to send the message to.
            media (List[Union[InputMediaPhoto, InputMediaVideo, InputMediaAudio]]): The media to send.
            reply_to_message_id (Optional[int], optional): The message ID to reply to. Defaults to None.
            reply_markup Optional[InlineKeyboardMarkup], optional): The reply keyboard markup (buttons).

        Returns:
            List[Message]: The list of messages.
        """
        data = await make_post(
            self.requests_base + "/sendMediaGroup",
            data={
                "chat_id": chat_id,
                "media": media,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": reply_markup.to_dict() if reply_markup else None,
            },
        )
        return [Message(**pythonize(msg)) for msg in data["result"]]

    async def send_location(
            self,
            chat_id: int,
            latitude: float,
            longitude: float,
            horizontal_accuracy: Optional[float] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
    ) -> Message:
        """Send a location to a chat.

        Args:
            chat_id (int): The chat to send the message to.
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.
            horizontal_accuracy (Optional[float], optional): The horizontal accuracy of the location.
            reply_to_message_id (Optional[int], optional): The message ID to reply to. Defaults to None.
            reply_markup Optional[InlineKeyboardMarkup], optional): The reply keyboard markup (buttons).

        Returns:
            Message: The message.
        """
        data = await make_post(
            self.requests_base + "/sendLocation",
            data={
                "chat_id": chat_id,
                "latitude": latitude,
                "longitude": longitude,
                "horizontal_accuracy": horizontal_accuracy,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": reply_markup.to_dict() if reply_markup else None,
            },
        )
        return Message(**pythonize(data["result"]))

    async def send_contact(
            self,
            chat_id: int,
            phone_number: str,
            first_name: str,
            last_name: Optional[str] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
    ) -> Message:
        """Send a contact to a chat.

        Args:
            chat_id (int): The chat to send the message to.
            phone_number (str): The phone number of the contact.
            first_name (str): The first name of the contact.
            last_name (Optional[str], optional): The last name of the contact.
            reply_to_message_id (Optional[int], optional): The message ID to reply to. Defaults to None.
            reply_markup Optional[InlineKeyboardMarkup], optional): The reply keyboard markup (buttons).

        Returns:
            Message: The message.
        """
        data = await make_post(
            self.requests_base + "/sendContact",
            data={
                "chat_id": chat_id,
                "phone_number": phone_number,
                "first_name": first_name,
                "last_name": last_name,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": reply_markup.to_dict() if reply_markup else None,
            },
        )
        return Message(**pythonize(data["result"]))

    async def send_invoice(
            self,
            chat_id: Union[str, int],
            title: str,
            description: str,
            payload: str,
            provider_token: str,
            prices: list[LabeledPrice],
            photo_url: Optional[str] = None,
            reply_to_message_id: Optional[int] = None,
    ) -> Message:
        """Sends a message including a invoice for user to pay.

        Args:
            chat_id (Union[str, int]): The chat to send the message to.
            title (str): The title of the invoice.
            description (str): The description of the invoice.
            payload (str): The payload of the invoice.
            provider_token (str): The provider token.
            prices (List[LabeledPrice]): The prices of the invoice.
            photo_url (Optional[str], optional): The photo url of the invoice.
            reply_to_message_id (Optional[int], optional): The message ID to reply to. Defaults to None.

        Returns:
            Message: The message.
        """
        new_prices = [price.json for price in prices]
        data = await make_post(
            self.requests_base + "/sendInvoice",
            data={
                "chat_id": chat_id,
                "title": title,
                "description": description,
                "payload": payload,
                "provider_token": provider_token,
                "prices": new_prices,
                "photo_url": photo_url,
                "reply_to_message_id": reply_to_message_id,
            },
        )
        return Message(**pythonize(data["result"]))

    async def get_file(self, file_id: str) -> File:
        """Get a file from the Bale servers.

        Args:
            file_id (str): The file ID.

        Returns:
            File: The file.
        """
        data = await make_post(
            self.requests_base + "/getFile", data={"file_id": file_id}
        )
        return File(**pythonize(data["result"]))

    async def answer_callback_query(
            self,
            callback_query_id: str,
            text: Optional[str] = None,
            show_alert: Optional[bool] = None,
    ) -> bool:
        """Answer a callback query.

        Args:
            callback_query_id (str): The callback query ID.
            text (Optional[str], optional): The text of the answer.
            show_alert (Optional[bool], optional): Whether the answer should be shown.

        Returns:
            bool: Whether the answer was shown.
        """
        data = await make_post(
            self.requests_base + "/answerCallbackQuery",
            data={
                "callback_query_id": callback_query_id,
                "text": text,
                "show_alert": show_alert,
            },
        )
        return data.get("ok", False)

    async def ban_chat_member(self, chat_id: int, user_id: int) -> bool:
        """Ban a user from a chat.

        Args:
            chat_id (int): The chat to ban.
            user_id (int): The user to ban.

        Returns:
            bool: Whether the ban was successful.
        """
        data = await make_post(
            self.requests_base + "/banChatMember",
            data={"chat_id": chat_id, "user_id": user_id},
        )
        try:
            return data.get("ok", False)
        except AttributeError:
            raise ForbiddenException("You cannot ban this member!")

    async def unban_chat_member(self, chat_id: int, user_id: int) -> bool:
        """Unban a user from a chat.

        Args:
            chat_id (int): The chat to unban.
            user_id (int): The user to unban.

        Returns:
            bool: Whether the unban was successful.
        """
        data = await make_post(
            self.requests_base + "/unbanChatMember",
            data={"chat_id": chat_id, "user_id": user_id},
        )
        return data.get("ok", False)

    async def kick_chat_member(self, chat_id: int, user_id: int) -> bool:
        """kick a user from a specified chat

        Args:
            chat_id (int): The chat to kick.
            user_id (int): The user to kick.

        Returns:
            bool: Whether the kick was successful.
        """
        try:
            await self.ban_chat_member(chat_id, user_id)
            await self.unban_chat_member(chat_id, user_id)
            return True
        except:
            return False

    async def get_chat_member(self, chat_id: int, user_id: int) -> ChatMember:
        """Get a chat member.

        Args:
            chat_id (int): The chat to get.
            user_id (int): The user to get.

        Returns:
            ChatMember: The chat member.
        """
        data = await make_post(
            self.requests_base + "/getChatMember",
            data={"chat_id": chat_id, "user_id": user_id},
        )

        temp = data.get("result")
        temp["chat"] = await self.get_chat(chat_id)
        temp["client"] = self
        data = temp

        return ChatMember(**pythonize(data))
    
    async def is_user_admin(self, chat_id: int, user_id: int) -> bool:
        """Checks if a user is admin in a chat

        Args:
            chat_id (int): The chat to get.
            user_id (int): The user to get.

        Returns:
            bool: Whether the user is admin in a chat.
        """
        chat_user = await self.get_chat_member(chat_id, user_id)
        if chat_user.status in ['creator', 'administrator']:
            return True
        else:
            return False
        
    async def user_has_permissions(self, chat_id: int, user_id: int, permissions: ChatPermissions) -> bool:
        """checks if a user has a specified permission

        Args:
            chat_id (int): The chat to get.
            user_id (int): The user to get.
            permissions (ChatPermissions): The permissions to check.

        Returns:
            bool: Whether the user has a specified permission.
        """
        member = self.get_chat_member(chat_id, user_id)
        if member.inputs[permissions.value]: 
            return True
        else: 
            return False

    async def promote_chat_member(
            self,
            chat_id: int,
            user_id: int,
            can_change_info: Optional[bool] = None,
            can_post_messages: Optional[bool] = None,
            can_edit_messages: Optional[bool] = None,
            can_delete_messages: Optional[bool] = None,
            can_invite_users: Optional[bool] = None,
            can_restrict_members: Optional[bool] = None,
            can_pin_messages: Optional[bool] = None,
            can_promote_members: Optional[bool] = None,
    ) -> bool:
        """Promote a user in a chat.

        Args:
            chat_id (int): The chat to get.
            user_id (int): The user to get.
            can_change_info (Optional[bool], optional): Whether the user can change the information.
            can_post_messages (Optional[bool], optional): Whether the user can post messages.
            can_edit_messages (Optional[bool], optional): Whether the user can edit messages.
            can_delete_messages (Optional[bool], optional): Whether the user can delete messages.
            can_invite_users (Optional[bool], optional): Whether the user can invite users.
            can_restrict_members (Optional[bool], optional): Whether the user can restrict members.
            can_pin_messages (Optional[bool], optional): Whether the user can pin messages.
            can_promote_members (Optional[bool], optional): Whether the user can promote members.

        Returns:
            bool: Whether the user has a specified permission.
        """
        data = await make_post(
            self.requests_base + "/promoteChatMember",
            data={
                "chat_id": chat_id,
                "user_id": user_id,
                "can_change_info": can_change_info,
                "can_post_messages": can_post_messages,
                "can_edit_messages": can_edit_messages,
                "can_delete_messages": can_delete_messages,
                "can_invite_users": can_invite_users,
                "can_restrict_members": can_restrict_members,
                "can_pin_messages": can_pin_messages,
                "can_promote_members": can_promote_members,
            },
        )
        return data.get("ok", False)

    async def set_chat_photo(self, chat_id: int, photo: InputFile) -> bool:
        """Set a new profile photo for the chat.

        Args:
            chat_id (int): The chat to get.
            photo (InputFile): The photo to set.

        Returns:
            bool: Whether the photo was set.
        """
        data = await make_post(
            self.requests_base + "/setChatPhoto",
            data={"chat_id": chat_id, "photo": photo},
        )
        return data.get("ok", False)

    async def leave_chat(self, chat_id: int) -> bool:
        """Leave a group, supergroup or channel.

        Args:
            chat_id (int): The chat to get.

        Returns:
            bool: Whether the chat was leaved.
        """
        data = await make_post(
            self.requests_base + "/leaveChat", data={"chat_id": chat_id}
        )
        return data.get("ok", False)

    async def is_joined(self, user_id: int, chat_id: int) -> bool:
        """Check if a user is joined to a chat.

        Args:
            user_id (int): The user to get.
            chat_id (int): The chat to get.

        Returns:
            bool: Whether the user is joined to a chat.
        """
        data = await make_post(
            self.requests_base + "/getChatMember",
            data={"chat_id": chat_id, "user_id": user_id},
        )
        return data.get("result", {}).get("status") in ["member", "creator", "administrator"]

    async def get_chat(self, chat_id: int) -> Chat:
        """Get up to date information about the chat.

        Args:
            chat_id (int): The chat to get.

        Returns:
            Chat: The chat.
        """
        data = await make_post(
            self.requests_base + "/getChat", data={"chat_id": chat_id}
        )

        temp = data.get("result")
        temp["client"] = self
        data = temp
        return Chat(**pythonize(data))

    @staticmethod
    async def get_ble_ir_page(username_or_phone_number: str) -> PeerData:
        """Get BleIR user/group information.

        Args:
            username_or_phone_number (str): The username or phone number.

        Returns:
            PeerData: The BleIR user/group information.
        """
        url = f"https://ble.ir/{username_or_phone_number}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                req = await response.text()

        if """<p class="__404_title__lxIKL">گفتگوی مورد نظر وجود ندارد.</p>""" in req:
            return PeerData(
                is_ok=False,
                avatar=None,
                description=None,
                name=None,
                is_bot=None,
                is_verified=None,
                is_private=None,
                members=None,
                last_message=None,
                user_id=None,
                username=None,
            )

        soup = BeautifulSoup(req, "html.parser")
        json_data = {}

        try:
            json_script = soup.find("script", id="__NEXT_DATA__").text
            json_data = loads(json_script)
            page_props = json_data.get("props", {}).get("pageProps", {})
            user_data = page_props.get("user", {})
            group_data = page_props.get("group", {})
            messages = page_props.get("messages", [])
        except (AttributeError, KeyError, JSONDecodeError):
            pass

        try:
            avatar = soup.find("img", class_="Avatar_img___C2_3")["src"]
        except (AttributeError, KeyError):
            avatar = None

        try:
            description = soup.find("div", class_="Profile_description__YTAr_").text
        except AttributeError:
            description = None

        try:
            name = soup.find("h1", class_="Profile_name__pQglx").text
        except AttributeError:
            name = None

        is_bot = user_data.get("isBot", False)
        is_verified = user_data.get("isVerified", group_data.get("isVerified", False))
        is_private = user_data.get("isPrivate", group_data.get("isPrivate", False))
        members = group_data.get("members")
        username = user_data.get("nick")
        user_id = page_props.get("peer", {}).get("id")

        last_message = None
        if messages:
            try:
                last_msg = messages[-1]["message"]
                last_message = (
                        last_msg.get("documentMessage", {}).get("caption", {}).get("text")
                        or last_msg.get("textMessage", {}).get("text")
                )
                if last_message:
                    last_message = last_message.replace("&zwnj;", "")
            except (KeyError, IndexError):
                pass

        return PeerData(
            True,
            avatar,
            description,
            name,
            is_bot,
            is_verified,
            is_private,
            members,
            last_message,
            user_id,
            username
        )

    async def get_chat_members_count(self, chat_id: int) -> int:
        """Get the number of members in a chat.

        Args:
            chat_id (int): The chat to get.

        Returns:
            int: The number of members in a chat.
        """
        data = await make_post(
            self.requests_base + "/getChatMembersCount", data={"chat_id": chat_id}
        )
        return data.get("result", 0)

    async def pin_chat_message(self, chat_id: int, message_id: int) -> bool:
        """Pin a message in a chat.

        Args:
            chat_id (int): The chat to get.
            message_id (int): The message to pin.

        Returns:
            bool: Whether the message was pinned.
        """
        data = await make_post(
            self.requests_base + "/pinChatMessage",
            data={"chat_id": chat_id, "message_id": message_id},
        )
        return data.get("ok", False)

    async def unpin_chat_message(self, chat_id: int, message_id: int) -> bool:
        """Unpin a message in a chat.

        Args:
            chat_id (int): The chat to get.
            message_id (int): The message to unpin.

        Returns:
            bool: Whether the message was unpinned.
        """
        data = await make_post(
            self.requests_base + "/unpinChatMessage", data={"chat_id": chat_id, "message_id": message_id}
        )
        return data.get("ok", False)

    async def unpin_all_chat_messages(self, chat_id: int) -> bool:
        """Unpin all messages in a chat.

        Args:
            chat_id (int): The chat to get.

        Returns:
            bool: Whether the message was unpinned.
        """
        data = await make_post(
            self.requests_base + "/unpinAllChatMessages", data={"chat_id": chat_id}
        )
        return data.get("ok", False)

    async def set_chat_title(self, chat_id: int, title: str) -> bool:
        """Change the title of a chat.

        Args:
            chat_id (int): The chat to get.
            title (str): The new title.

        Returns:
            bool: Whether the title was changed.
        """
        data = await make_post(
            self.requests_base + "/setChatTitle",
            data={"chat_id": chat_id, "title": title},
        )
        return data.get("ok", False)

    async def set_chat_description(self, chat_id: int, description: str) -> bool:
        """Change the description of a chat.

        Args:
            chat_id (int): The chat to get.
            description (str): The new description.

        Returns:
            bool: Whether the description was changed.
        """
        data = await make_post(
            self.requests_base + "/setChatDescription",
            data={"chat_id": chat_id, "description": description},
        )
        return data.get("ok", False)

    async def delete_chat_photo(self, chat_id: int) -> bool:
        """Delete a chat photo.

        Args:
            chat_id (int): The chat to get.

        Returns:
            bool: Whether the photo was deleted.
        """
        data = await make_post(
            self.requests_base + "/deleteChatPhoto", data={"chat_id": chat_id}
        )
        return data.get("ok", False)

    async def edit_message(
            self,
            chat_id: Union[int, str],
            message_id: int,
            text: str,
            reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Edits a message in a specified chat

        Args:
            chat_id (int): The chat to get.
            message_id (int): The message to get.
            text (str): The text to edit.
            reply_markup (InlineKeyboardMarkup, optional): the reply markup to use. Defaults to None.

        Returns:
            Message: The edited message.
        """
        data = await make_post(
            self.requests_base + "/editMessageText",
            data={
                "chat_id": chat_id,
                "message_id": message_id,
                "text": text,
                "reply_markup": reply_markup.to_dict() if reply_markup else None,
            },
        )
        return Message(**pythonize(data["result"]))

    async def create_chat_invite_link(self, chat_id: int) -> str:
        """Create an additional invite link for a chat.

        Args:
            chat_id (int): The chat to get.

        Returns:
            str: The invite link.
        """
        data = await make_post(
            self.requests_base + "/createChatInviteLink", data={"chat_id": chat_id}
        )
        return data.get("result", "")

    async def revoke_chat_invite_link(self, chat_id: int, invite_link: str) -> str:
        """Revoke an invite link created by the bot.

        Args:
            chat_id (int): The chat to get.
            invite_link (str): The invite link to revoke.

        Returns:
            str: The revoked invite link.
        """
        data = await make_post(
            self.requests_base + "/revokeChatInviteLink",
            data={"chat_id": chat_id, "invite_link": invite_link},
        )
        return data.get("result", "")

    async def export_chat_invite_link(self, chat_id: int) -> str:
        """Generate a new primary invite link for a chat.

        Args:
            chat_id (int): The chat to get.

        Returns:
            str: The invite link.
        """
        data = await make_post(
            self.requests_base + "/exportChatInviteLink", data={"chat_id": chat_id}
        )
        return data.get("result", "")

    async def send_chat_action(self, chat_id: int, action: ChatAction) -> bool:
        """Tell the user that something is happening on the bot's side.

        Args:
            chat_id (int): The chat to get.
            action (ChatAction): The action to send.

        Returns:
            bool: Whether the action was sent.
        """
        data = await make_post(
            self.requests_base + "/sendChatAction",
            data={"chat_id": str(chat_id), "action": action.value},
        )
        return data.get("ok", False)

    async def wait_for(self, update_type: UpdatesTypes, check=None):
        """Wait until a specified update

        Args:
            update_type (UpdatesTypes): The update to wait for.
            check (Callable, optional): The check method to check.
        """
        future = asyncio.get_running_loop().create_future()
        self._waiters.append((update_type, check, future))
        return await future

    async def process_update(self, update: Dict[str, Any]) -> None:
        """Process a single update and call registered handlers.

        Args:
            update (Dict[str, Any]): The update to process.

        Returns:
            None
        """
        update_id = update.get("update_id")
        if update_id:
            self.last_update_id = update_id + 1

        
        if self.check_defined_message:
            try:
                update_raw = update.get('message', {})
                if update_raw.get("text") in self.defined_messages:
                    await self.send_message(
                        update_raw.get('chat', {}).get('id'),
                        self.defined_messages.get(update_raw.get("text")),
                        update_raw.get('message_id')
                    )
            except Exception as e:
                print(f"Error processing defined message: {e}")

        
        for waiter in list(self._waiters):
            w_type, check, future = waiter
            if w_type.value in update:
                event_data = update[w_type.value]
                try:
                    event = self._convert_event(w_type, event_data)
                    if check is None or check(event):
                        if not future.done():
                            future.set_result(event)
                        self._waiters.remove(waiter)
                        return
                except Exception as e:
                    print(f"Error in waiter conversion: {e}")
                    continue

        
        for handler in self.handlers:
            handler_type = handler["type"]
            update_type_key = handler_type.value

            
            if handler_type == UpdatesTypes.COMMAND:
                
                if "message" not in update or "text" not in update["message"]:
                    continue

                message_text = update["message"]["text"]
                if not message_text.startswith("/"):
                    continue

                
                command_parts = message_text[1:].split()
                if not command_parts:
                    continue

                actual_command = command_parts[0].split('@')[0]  
                expected_command = handler.get("command", "")

                if actual_command != expected_command:
                    continue

                
                try:
                    event = self._convert_event(UpdatesTypes.MESSAGE, update["message"])
                except Exception as e:
                    print(f"Error converting command event: {e}")
                    continue

            else:
                
                if update_type_key not in update:
                    continue

                raw_event = update[update_type_key]
                try:
                    event = self._convert_event(handler_type, raw_event)
                except Exception as e:
                    print(f"Error converting event for handler {handler_type}: {e}")
                    continue

            
            flt = handler.get("filter")
            if flt is not None:
                if callable(flt):
                    try:
                        if not flt(event):
                            continue
                    except Exception as e:
                        print(f"[Filter Error] {e}")
                        continue
                elif isinstance(flt, Filters):
                    if not hasattr(event, flt.value):
                        continue

            
            try:
                if asyncio.iscoroutinefunction(handler["callback"]):
                    asyncio.create_task(handler["callback"](event))
                else:
                    handler["callback"](event)
            except Exception as e:
                print(f"Error executing handler: {e}")
                
    def _convert_event(self, handler_type: UpdatesTypes, event_data: Dict[str, Any]) -> Any:
        """Convert raw event data to appropriate object type.

        Args:
            handler_type (UpdatesTypes): The event to convert.
            event_data (Dict[str, Any]): The event to convert.

        Returns:
            Any: The converted event.
        """
        chat = Chat(**event_data.get("chat"))
        kwargs = {"client": self, "chat": chat}

        try:
            if handler_type in [UpdatesTypes.MESSAGE, UpdatesTypes.MESSAGE_EDITED, UpdatesTypes.COMMAND]:
                return Message(kwargs=kwargs, **pythonize(event_data))
            elif handler_type == UpdatesTypes.CALLBACK_QUERY:
                return CallbackQuery(kwargs=kwargs, **pythonize(event_data))
            elif handler_type == UpdatesTypes.PRE_CHECKOUT_QUERY:
                return PreCheckoutQuery(kwargs=kwargs, **pythonize(event_data))
            elif handler_type == UpdatesTypes.MEMBER_JOINED:
                if "new_chat_member" in event_data:
                    return ChatMember(kwargs=kwargs, **pythonize(event_data["new_chat_member"]))
                return Message(kwargs=kwargs, **pythonize(event_data))
            elif handler_type == UpdatesTypes.MEMBER_LEFT:
                if "left_chat_member" in event_data:
                    return ChatMember(kwargs=kwargs, **pythonize(event_data["left_chat_member"]))
                return Message(kwargs=kwargs, **pythonize(event_data))
            elif handler_type == UpdatesTypes.SUCCESSFUL_PAYMENT:
                if "successful_payment" in event_data:
                    return SuccessfulPayment(kwargs=kwargs, **pythonize(event_data["successful_payment"]))
                return Message(kwargs=kwargs, **pythonize(event_data))
            else:
                return event_data
        except Exception as e:
            print(f"Error converting event {handler_type}: {e}")
            return event_data

    def base_handler_decorator(self, update_type: UpdatesTypes):
        """Base decorator for handling different types of updates.

        Args:
            update_type (UpdatesTypes): The update to process.

        Returns:
            Callable: The decorated handler.
        """

        def wrapper(filter: Optional[Filters] = None):
            def decorator(callback: Callable[[Any], Union[None, Awaitable[None]]]):
                self.add_handler(update_type, callback, filter)
                return callback

            return decorator

        return wrapper

    def on_command(self, command: str, filter: Optional[Filters] = None):
        """Decorator for handling command updates."""

        def decorator(callback: Callable[[Any], Union[None, Awaitable[None]]]):
            self.add_handler(UpdatesTypes.COMMAND, callback, filter, command=command)
            return callback

        return decorator

    def on_message(self, filter: Optional[Filters] = None):
        """Decorator for handling new message updates."""
        return self.base_handler_decorator(UpdatesTypes.MESSAGE)(filter)

    def on_edited_message(self, filter: Optional[Filters] = None):
        """Decorator for handling edited message updates."""
        return self.base_handler_decorator(UpdatesTypes.MESSAGE_EDITED)(filter)

    def on_callback_query(self, filter: Optional[Filters] = None):
        """Decorator for handling callback query updates."""
        return self.base_handler_decorator(UpdatesTypes.CALLBACK_QUERY)(filter)

    def on_new_members(self, filter: Optional[Filters] = None):
        """Decorator for handling new chat members updates."""
        return self.base_handler_decorator(UpdatesTypes.MEMBER_JOINED)(filter)

    def on_members_left(self, filter: Optional[Filters] = None):
        """Decorator for handling members left updates."""
        return self.base_handler_decorator(UpdatesTypes.MEMBER_LEFT)(filter)

    def on_pre_checkout_query(self, filter: Optional[Filters] = None):
        """Decorator for handling pre-checkout query updates."""
        return self.base_handler_decorator(UpdatesTypes.PRE_CHECKOUT_QUERY)(filter)

    def on_photo(self, filter: Optional[Filters] = None):
        """Decorator for handling photo updates."""
        return self.base_handler_decorator(UpdatesTypes.PHOTO)(filter)

    def on_successful_payment(self, filter: Optional[Filters] = None):
        """Decorator for handling successful payment updates."""
        return self.base_handler_decorator(UpdatesTypes.SUCCESSFUL_PAYMENT)(filter)

    def add_handler(self, update_type: UpdatesTypes, callback: Callable, filter: Optional[Filters] = None, **kwargs):
        """Register a handler for specific update type.

        Args:
            update_type (UpdatesTypes): The update to process.
            callback (Callable): The callback to handle.
            filter (Optional[Filters]): The filter to handle.
            **kwargs: The kwargs to pass to the callback.

        Returns:
            Callable: The decorated handler.
        """
        handler_data = {
            "type": update_type,
            "callback": callback,
            "filter": filter,
        }
        handler_data.update(kwargs)
        self.handlers.append(handler_data)

    def remove_handler(self, callback: Callable) -> None:
        """Remove a handler from the list of handlers.

        Args:
            callback (Callable): The callback to remove.

        """
        self.handlers = [
            handler for handler in self.handlers if handler["callback"] != callback
        ]

    def remove_all_handlers(self) -> None:
        """Remove all handlers from the list of handlers."""
        self.handlers = []

    async def start_polling(self, timeout: int = 30, limit: int = 100) -> None:
        """Start polling updates from the server.

        Args:
            timeout (int): Time to wait for updates.
            limit (int): Number of updates to poll.
        """
        if self.running:
            raise RuntimeError("Client is already running")

        self.running = True
        while self.running:
            try:
                updates = await self.get_updates(
                    offset=self.last_update_id, limit=limit, timeout=timeout
                )

                for update in updates:
                    await self.process_update(update)

            except Exception as e:
                print(f"Error in polling: {e}")
                await asyncio.sleep(1)
                
    async def stop_polling(self) -> None:
        """Stop polling updates."""
        self.running = False

    def run(self, timeout: int = 30, limit: int = 100) -> None:
        """Run the client.

        Args:
            timeout (int): Time to wait for updates.
            limit (int): Number of updates to poll.

        """
        try:
            asyncio.run(self.start_polling(timeout, limit))
        except KeyboardInterrupt:
            print("Bot stopped by user")

    async def stop(self) -> None:
        """Stop the client."""
        await self.stop_polling()

    async def handle_webhook_update(self, update_data: Dict[str, Any]) -> None:
        """Process an update received via webhook."""
        await self.process_update(update_data)
