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
import asyncio
from enum import Enum
from ..objects.enums import UpdatesTypes, ChatAction, ChatType
from ..filters import Filters, equals
from ..StateMachine import StateMachine
from ..exceptions import NotFoundException, InvalidTokenException, PyroBaleException


class Client:
    """A client for interacting with the Bale messenger API.

    Args:
        token (str): The bot token.
        base_url (str, optional): The base URL for the API. Defaults to "https://tapi.bale.ai/bot".
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

    async def get_updates(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        timeout: Optional[int] = None,
    ) -> List[Dict]:
        """Get updates from the Bale API.

        Args:
            offset (int, optional): The offset of the updates to get. Defaults to None.
            limit (int, optional): The maximum number of updates to get. Defaults to None.
            timeout (int, optional): The timeout for the request. Defaults to None.
        Returns:
            List[Dict]: The updates.
        """
        data = await make_get(
            self.requests_base
            + f"/getUpdates?offset={offset}&limit={limit}&timeout={timeout}"
        )
        if data['ok']:
            if 'result' in data.keys():
                return data["result"]
            else:
                if data['error_code'] == 403:
                    raise InvalidTokenException("Forbidden 403 : --ENTERED TOKEN IS NOT VALID--")

    async def set_webhook(self, url: str) -> bool:
        """Set the webhook for the bot.

        Args:
            url (str): The URL to set the webhook to.
        Returns:
            bool: True if the webhook was set successfully, False otherwise.
        """
        data = await make_post(self.requests_base + "/setWebhook", data={"url": url})
        return data["result"]

    async def get_webhook_info(self) -> Dict:
        """Get the webhook information for the bot.

        Returns:
            Dict: The webhook information.
        """
        data = await make_get(self.requests_base + "/getWebhookInfo")
        return data["result"]

    async def get_me(self) -> User:
        """Get information about the bot.

        Returns:
            User: The information about the bot.
        """
        data = await make_get(self.requests_base + "/getMe")
        return User(**data["result"])

    async def logout(self) -> bool:
        """Log out the bot.

        Returns:
            bool: True if the bot was logged out successfully, False otherwise.
        """
        data = await make_get(self.requests_base + "/logOut")
        return data["result"]

    async def close(self) -> bool:
        """Close the bot.

        Returns:
            bool: True if the bot was closed successfully, False otherwise.
        """
        data = await make_get(self.requests_base + "/close")
        return data["result"]

    async def send_message(
        self,
        chat_id: int,
        text: str,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
    ) -> Message:
        """Send a message to a chat.

        Args:
            chat_id (int): The ID of the chat to send the message to.
            text (str): The text of the message.
            reply_to_message_id (int, optional): The ID of the message to reply to. Defaults to None.
            reply_markup (Union[InlineKeyboardMarkup, ReplyKeyboardMarkup], optional): The reply markup to use. Defaults to None.
        Returns:
            Message: The message that was sent.
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
        return Message(**pythonize(data["result"]))

    async def forward_message(
        self, chat_id: int, from_chat_id: int, message_id: int
    ) -> Message:
        """Forward a message to a chat.

        Args:
            chat_id (int): The ID of the chat to forward the message to.
            from_chat_id (int): The ID of the chat to forward the message from.
            message_id (int): The ID of the message to forward.
        Returns:
            Message: The message that was forwarded.
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
        """Copy a message to a chat.

        Args:
            chat_id (int): The ID of the chat to copy the message to.
            from_chat_id (int): The ID of the chat to copy the message from.
            message_id (int): The ID of the message to copy.
        Returns:
            Message: The message that was copied.
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
            chat_id (Union[int, str]): The ID of the chat to send the photo to.
            photo (Union[InputFile, str]): The photo to send.
            caption (str, optional): The caption of the photo. Defaults to None.
            reply_to_message_id (int, optional): The ID of the message to reply to. Defaults to None.
            reply_markup (Union[InlineKeyboardMarkup, ReplyKeyboardMarkup], optional): The reply markup to use. Defaults to None.
        Returns:
            Message: The message that was sent.
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
            chat_id (int): The ID of the chat to send the audio to.
            audio (Union[InputFile, str]): The audio to send.
            caption (str, optional): The caption of the audio. Defaults to None.
            reply_to_message_id (int, optional): The ID of the message to reply to. Defaults to None.
            reply_markup (Union[InlineKeyboardMarkup, ReplyKeyboardMarkup], optional): The reply markup to use. Defaults to None.
        Returns:
            Message: The message that was sent.
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
            chat_id (int): The ID of the chat to send the document to.
            document (Union[InputFile, str]): The document to send.
            caption (str, optional): The caption of the document. Defaults to None.
            reply_to_message_id (int, optional): The ID of the message to reply to. Defaults to None.
            reply_markup (Union[InlineKeyboardMarkup, ReplyKeyboardMarkup], optional): The reply markup to use. Defaults to None.
        Returns:
            Message: The message that was sent.
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
            chat_id (int): The ID of the chat to send the video to.
            video (Union[InputFile, str]): The video to send.
            caption (str, optional): The caption of the video. Defaults to None.
            reply_to_message_id (int, optional): The ID of the message to reply to. Defaults to None.
            reply_markup (Union[InlineKeyboardMarkup, ReplyKeyboardMarkup], optional): The reply markup to use. Defaults to None.
        Returns:
            Message: The message that was sent.
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
        """Send an animation to a chat.

        Args:
            chat_id (int): The ID of the chat to send the animation to.
            animation (Union[InputFile, str]): The animation to send.
            caption (str, optional): The caption of the animation. Defaults to None.
            reply_to_message_id (int, optional): The ID of the message to reply to. Defaults to None.
            reply_markup (Union[InlineKeyboardMarkup, ReplyKeyboardMarkup], optional): The reply markup to use. Defaults to None.
        Returns:
            Message: The message that was sent.
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
            chat_id (int): The ID of the chat to send the voice message to.
            voice (Union[InputFile, str]): The voice message to send.
            caption (str, optional): The caption of the voice message. Defaults to None.
            reply_to_message_id (int, optional): The ID of the message to reply to. Defaults to None.
            reply_markup (Union[InlineKeyboardMarkup, ReplyKeyboardMarkup], optional): The reply markup to use. Defaults to None.
        Returns:
            Message: The message that was sent.
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
            chat_id (int): The ID of the chat to send the media group to.
            media (List[Union[InputMediaPhoto, InputMediaVideo, InputMediaAudio]]): The media group to send.
            reply_to_message_id (int, optional): The ID of the message to reply to. Defaults to None.
            reply_markup (Union[InlineKeyboardMarkup, ReplyKeyboardMarkup], optional): The reply markup to use. Defaults to None.
        Returns:
            List[Message]: The messages that were sent.
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
        return Message(**pythonize(data["result"]))

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
            chat_id (int): The ID of the chat to send the location to.
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.
            reply_to_message_id (int, optional): The ID of the message to reply to. Defaults to None.
            reply_markup (Union[InlineKeyboardMarkup, ReplyKeyboardMarkup], optional): The reply markup to use. Defaults to None.
        Returns:
            Message: The message that was sent.
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
            chat_id (int): The ID of the chat to send the contact to.
            phone_number (str): The phone number of the contact.
            first_name (str): The first name of the contact.
            last_name (str, optional): The last name of the contact. Defaults to None.
            reply_to_message_id (int, optional): The ID of the message to reply to. Defaults to None.
            reply_markup (Union[InlineKeyboardMarkup, ReplyKeyboardMarkup], optional): The reply markup to use. Defaults to None.
        Returns:
            Message: The message that was sent.
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
            chat_id (string OR integer): unique chat id to send the invoice
            title (string): the title of invoice
            description (string): desciption of invoice, you can explain the invoice here
            payload (string): payload of invoice, user will not see this, it'll be returned after successful payment
            provider_token (string): Wallet token or card number of receiver
            prices (list of LabledPrice): a list of prices that user must pay
            photo_url (Optional: string): url of a photo that will be sent with invoice
            reply_to_message_id (Optional: int): message id to reply that

        Returns:
            Message: returns the sent message with invoice
        """
        new_prices = []
        for price in prices:
            new_prices.append(price.json)
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
            file_id (str): The ID of the file to get.
        Returns:
            File: The file that was retrieved.
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
    ):
        """Answer a callback query.

        Args:
            callback_query_id (str): The ID of the callback query to answer.
            text (str, optional): The text to show to the user. Defaults to None.
            show_alert (bool, optional): Whether to show an alert to the user. Defaults to None.
        Returns:
            bool: Whether the callback query was answered successfully.
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
            chat_id (int): The ID of the chat to ban the user from.
            user_id (int): The ID of the user to ban.
        Returns:
            bool: Whether the user was banned successfully
        """

        data = await make_post(
            self.requests_base + "/banChatMember",
            data={"chat_id": chat_id, "user_id": user_id},
        )
        return data.get("ok", False)

    async def unban_chat_member(self, chat_id: int, user_id: int) -> bool:
        """Unban a user from a chat.

        Args:
            chat_id (int): The ID of the chat to unban the user from.
            user_id (int): The ID of the user to unban.
        Returns:
            bool: Whether the user was unbanned successfully.
        """
        data = await make_post(
            self.requests_base + "/unbanChatMember",
            data={"chat_id": chat_id, "user_id": user_id},
        )
        return data.get("ok", False)

    async def get_chat_member(self, chat_id: int, user_id: int) -> ChatMember:
        """Get a chat member.

        Args:
            chat_id (int): The ID of the chat to get the member from.
            user_id (int): The ID of the user to get.
        Returns:
            ChatMember: The chat member that was retrieved.
        """
        data = await make_post(
            self.requests_base + "/getChatMember",
            data={"chat_id": chat_id, "user_id": user_id},
        )
        return ChatMember(
            kwargs={"client": self, "chat": chat_id}, **pythonize(data["result"])
        )

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
    ):
        """Promote a user in a chat.

        Args:
            chat_id (int): The ID of the chat to promote the user in.
            user_id (int): The ID of the user to promote.
            can_change_info (bool, optional): Whether the user can change the chat info. Defaults to None.
            can_post_messages (bool, optional): Whether the user can post messages. Defaults to None.
            can_edit_messages (bool, optional): Whether the user can edit messages. Defaults to None.
            can_delete_messages (bool, optional): Whether the user can delete messages. Defaults to None.
            can_invite_users (bool, optional): Whether the user can invite users. Defaults to None.
            can_restrict_members (bool, optional): Whether the user can restrict members. Defaults to None.
            can_pin_messages (bool, optional): Whether the user can pin messages. Defaults to None.
            can_promote_members (bool, optional): Whether the user can promote members. Defaults to None.
        Returns:
            bool: Whether the user was promoted successfully.
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
            chat_id (int): Unique identifier for the target chat
            photo (InputFile): New chat photo

        Returns:
            bool: True on success
        """
        data = await make_post(
            self.requests_base + "/setChatPhoto",
            data={"chat_id": chat_id, "photo": photo},
        )
        return data.get("ok", False)

    async def leave_chat(self, chat_id: int) -> bool:
        """Leave a group, supergroup or channel.

        Args:
            chat_id (int): Unique identifier for the target chat

        Returns:
            bool: True on success
        """
        data = await make_post(
            self.requests_base + "/leaveChat", data={"chat_id": chat_id}
        )
        return data.get("ok", False)
    
    async def is_joined(self, user_id: int, chat_id: int) -> bool:
        """Check if a user is joined to a chat.
        
        Args:
            user_id (int): Unique identifier for the target chat
            chat_id (int): Unique identifier for the target chat
        
        Returns:
            bool: True if the user is joined to the chat, False otherwise
        """
        data = await make_post(
            self.requests_base + "/getChatMember",
            data={"chat_id": chat_id, "user_id": user_id},
        )
        return data.get("result", {}).get("status") in ["member", "creator", "administrator"]

    async def get_chat(self, chat_id: int) -> Chat:
        """Get up to date information about the chat.

        Args:
            chat_id (int): Unique identifier for the target chat

        Returns:
            Chat: Chat object with information about the chat
        """
        data = await make_post(
            self.requests_base + "/getChat", data={"chat_id": chat_id}
        )
        return Chat(**pythonize(data["result"]))

    async def get_chat_members_count(self, chat_id: int) -> int:
        """Get the number of members in a chat.

        Args:
            chat_id (int): Unique identifier for the target chat

        Returns:
            int: Number of members in the chat
        """
        data = await make_post(
            self.requests_base + "/getChatMembersCount", data={"chat_id": chat_id}
        )
        return data.get("result", 0)

    async def pin_chat_message(self, chat_id: int, message_id: int) -> bool:
        """Pin a message in a chat.

        Args:
            chat_id (int): Unique identifier for the target chat
            message_id (int): Identifier of a message to pin

        Returns:
            bool: True on success
        """
        data = await make_post(
            self.requests_base + "/pinChatMessage",
            data={"chat_id": chat_id, "message_id": message_id},
        )
        return data.get("ok", False)

    async def unpin_chat_message(self, chat_id: int) -> bool:
        """Unpin a message in a chat.

        Args:
            chat_id (int): Unique identifier for the target chat

        Returns:
            bool: True on success
        """
        data = await make_post(
            self.requests_base + "/unpinChatMessage", data={"chat_id": chat_id}
        )
        return data.get("ok", False)

    async def unpin_all_chat_messages(self, chat_id: int) -> bool:
        """Unpin all messages in a chat.

        Args:
            chat_id (int): Unique identifier for the target chat

        Returns:
            bool: True on success
        """
        data = await make_post(
            self.requests_base + "/unpinAllChatMessages", data={"chat_id": chat_id}
        )
        return data.get("ok", False)

    async def set_chat_title(self, chat_id: int, title: str) -> bool:
        """Change the title of a chat.

        Args:
            chat_id (int): Unique identifier for the target chat
            title (str): New chat title, 1-255 characters

        Returns:
            bool: True on success
        """
        data = await make_post(
            self.requests_base + "/setChatTitle",
            data={"chat_id": chat_id, "title": title},
        )
        return data.get("ok", False)

    async def set_chat_description(self, chat_id: int, description: str) -> bool:
        """Change the description of a chat.

        Args:
            chat_id (int): Unique identifier for the target chat
            description (str): New chat description, 0-255 characters

        Returns:
            bool: True on success
        """
        data = await make_post(
            self.requests_base + "/setChatDescription",
            data={"chat_id": chat_id, "description": description},
        )
        return data.get("ok", False)

    async def delete_chat_photo(self, chat_id: int) -> bool:
        """Delete a chat photo.

        Args:
            chat_id (int): Unique identifier for the target chat

        Returns:
            bool: True on success
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
            chat_id (int OR str): Unique identifier for the target chat
            message_id (int): Unique indentifier for the message you want to edit
            text (str): New text of message
            reply_markup (InlineKeyboardMarkup): Inline markup you can add or change in message

        Returns:
            Message: The object of edited message
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
            chat_id (int): Unique identifier for the target chat

        Returns:
            str: The new invite link
        """
        data = await make_post(
            self.requests_base + "/createChatInviteLink", data={"chat_id": chat_id}
        )
        return data.get("result", "")

    async def revoke_chat_invite_link(self, chat_id: int, invite_link: str) -> str:
        """Revoke an invite link created by the bot.

        Args:
            chat_id (int): Unique identifier for the target chat
            invite_link (str): The invite link to revoke

        Returns:
            str: The revoked invite link
        """
        data = await make_post(
            self.requests_base + "/revokeChatInviteLink",
            data={"chat_id": chat_id, "invite_link": invite_link},
        )
        return data.get("result", "")

    async def export_chat_invite_link(self, chat_id: int) -> str:
        """Generate a new primary invite link for a chat.

        Args:
            chat_id (int): Unique identifier for the target chat

        Returns:
            str: The new invite link
        """
        data = await make_post(
            self.requests_base + "/exportChatInviteLink", data={"chat_id": chat_id}
        )
        return data.get("result", "")

    async def send_chat_action(self, chat_id: int, action: ChatAction) -> bool:
        """Tell the user that something is happening on the bot's side.

        Args:
            chat_id (int): Unique identifier for the target chat
            action (ChatAction): Type of action to broadcast

        Returns:
            bool: True on success
        """
        data = await make_post(
            self.requests_base + "/sendChatAction",
            data={"chat_id": str(chat_id), "action": action.value},
        )
        return data.get("ok", False)

    async def wait_for(self, update_type: UpdatesTypes, check=None):
        """Wait until a specified update

        Args:
            update_type (UpdatesTypes): The type of update you're waiting for it.
            check: a condition that will be checked before passing.
        """
        future = asyncio.get_running_loop().create_future()
        self._waiters.append((update_type, check, future))
        return await future

    async def process_update(self, update: Dict[str, Any]) -> None:
        """Process a single update and call registered handlers.

        Args:
            update (Dict[str, Any]): The update to process
        """
        update_id = update.get("update_id")
        if update_id:
            self.last_update_id = update_id + 1

        for waiter in list(self._waiters):
            w_type, check, future = waiter
            if w_type.value in update:
                event = update[w_type.value]
                event = self._convert_event(w_type, event)
                if check is None or check(event):
                    if not future.done():
                        future.set_result(event)
                    self._waiters.remove(waiter)
                    return

        for handler in self.handlers:
            update_type = handler["type"].value
            if update_type in update:
                raw_event = update[update_type]
                event = self._convert_event(handler["type"], raw_event)
                
                if handler["type"] == UpdatesTypes.COMMAND:
                    if hasattr(event, 'text') and event.text and event.text.startswith('/'):
                        command_text = event.text[1:]
                        command_parts = command_text.split()
                        if command_parts:
                            actual_command = command_parts[0]
                            expected_command = handler.get("command", "")
                            
                            if actual_command != expected_command:
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
                    
                if asyncio.iscoroutinefunction(handler["callback"]):
                    asyncio.create_task(handler["callback"](event))
                else:
                    handler["callback"](event)



    def base_handler_decorator(self, update_type: UpdatesTypes):
        """Base decorator for handling different types of updates.

        Args:
            update_type (UpdatesTypes): The type of update to handle.

        Returns:
            Callable: A decorator function that registers the callback for the specified update type.
        """
        def wrapper(filter: Optional[Filters] = None):
            def decorator(callback: Callable[[Any], Union[None, Awaitable[None]]]):
                self.add_handler(update_type, callback, filter)
                return callback
            return decorator
        return wrapper
    
    def on_command(self, command: str, filter: Optional[Filters] = None):
        """Decorator for handling command updates.

        Args:
            command (str): The command to handle.
            filter (Optional[Filters]): An optional filter to apply to the command.
        Returns:
            Callable: A decorator function that registers the callback for the specified command.
        """
        def decorator(callback: Callable[[Any], Union[None, Awaitable[None]]]):
            self.add_handler(UpdatesTypes.COMMAND, callback, filter, command=command)
            return callback
        return decorator


    def on_message(self, filter: Optional[Filters] = None):
        """Decorator for handling new message updates.

        Returns:
            Callable: A decorator function that registers the callback for message updates.
        """
        return self.base_handler_decorator(UpdatesTypes.MESSAGE)(filter)


    def on_edited_message(self):
        """Decorator for handling edited message updates.

        Returns:
            Callable: A decorator function that registers the callback for edited message updates.
        """
        return self.base_handler_decorator(UpdatesTypes.MESSAGE_EDITED)

    def on_callback_query(self):
        """Decorator for handling callback query updates.

        Returns:
            Callable: A decorator function that registers the callback for callback query updates.
        """
        return self.base_handler_decorator(UpdatesTypes.CALLBACK_QUERY)

    def on_new_members(self):
        """Decorator for handling new chat members updates.

        Returns:
            Callable: A decorator function that registers the callback for new members updates.
        """
        return self.base_handler_decorator(UpdatesTypes.MEMBER_JOINED)

    def on_members_left(self):
        return self.base_handler_decorator(UpdatesTypes.MEMBER_LEFT)

    def on_pre_checkout_query(self):
        """Decorator for handling pre-checkout query updates.

        Returns:
            Callable: A decorator function that registers the callback for pre-checkout query updates.
        """
        return self.base_handler_decorator(UpdatesTypes.PRE_CHECKOUT_QUERY)

    def on_photo(self):
        """Decorator for handling photo updates.

        Returns:
            Callable: A decorator function that registers the callback for photo updates.
        """
        return self.base_handler_decorator(UpdatesTypes.PHOTO)

    def on_successful_payment(self):
        """Decorator for handling successful payment updates.

        Returns:
            Callable: A decorator function that registers the callback for successful payment updates.
        """
        return self.base_handler_decorator(UpdatesTypes.SUCCESSFUL_PAYMENT)
    
    def _convert_event(self, handler_type: UpdatesTypes, event: Dict[str, Any]) -> Any:
        """Convert raw event data to appropriate object type.

        Args:
            handler_type (UpdatesTypes): Type of the update
            event (Dict[str, Any]): Raw event data

        Returns:
            Any: Converted event object
        """
        if handler_type in (
            UpdatesTypes.MESSAGE,
            UpdatesTypes.MESSAGE_EDITED,
            UpdatesTypes.MEMBER_JOINED,
            UpdatesTypes.MEMBER_LEFT,
            UpdatesTypes.SUCCESSFUL_PAYMENT,
            UpdatesTypes.COMMAND
        ):
            if (
                event.get("new_chat_member", False)
                and handler_type == UpdatesTypes.MEMBER_JOINED
            ):
                return (
                    ChatMember(
                        kwargs={"client": self},
                        **pythonize(event.get("new_chat_member", {})),
                    ),
                    Chat(kwargs={"client": self}, **pythonize(event.get("chat", {}))),
                    Message(
                        kwargs={"client": self}, **pythonize(event.get("message", {}))
                    ),
                )
            elif (
                event.get("left_chat_member", False)
                and handler_type == UpdatesTypes.MEMBER_LEFT
            ):
                return (
                    ChatMember(
                        kwargs={"client": self},
                        **pythonize(event.get("left_chat_member", {})),
                    ),
                    Chat(kwargs={"client": self}, **pythonize(event.get("chat", {}))),
                    Message(
                        kwargs={"client": self}, **pythonize(event.get("message", {}))
                    ),
                )

            elif (
                event.get("successful_payment", False)
                and handler_type == UpdatesTypes.SUCCESSFUL_PAYMENT
            ):
                return Message(
                    **pythonize(event.get("successful_payment", {})),
                    kwargs={"client": self},
                )

            else:
                return Message(kwargs={"client": self}, **pythonize(event))

        elif handler_type == UpdatesTypes.CALLBACK_QUERY:
            return CallbackQuery(kwargs={"client": self}, **pythonize(event))

        elif handler_type == UpdatesTypes.PRE_CHECKOUT_QUERY:
            return PreCheckoutQuery(kwargs={"client": self}, **pythonize(event))

        return event


    def add_handler(self, update_type, callback, filter: Optional[Filters] = None, **kwargs):
        """Register a handler for specific update type.

        Args:
            update_type (UpdatesTypes): Type of update to handle
            callback (Callable): Function to call when update is received
        """
        data = {
            "type": update_type,
            "callback": callback,
            "filter": filter,
        }
        data.update(kwargs)
        self.handlers.append(data)


    def remove_handler(
        self, callback: Callable[[Any], Union[None, Awaitable[None]]]
    ) -> None:
        """Remove a handler from the list of handlers.

        Args:
            callback (Callable): Handler function to remove
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
            timeout (int, optional): Timeout in seconds for long polling. Defaults to 30.
            limit (int, optional): Maximum number of updates to retrieve. Defaults to 100.

        Raises:
            RuntimeError: If client is already running
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
                raise e

    async def stop_polling(self) -> None:
        """Stop polling updates."""
        self.running = False

    def run(self, timeout: int = 30, limit: int = 100) -> None:
        """Run the client.

        Args:
            timeout (int, optional): Timeout in seconds for long polling. Defaults to 30.
            limit (int, optional): Maximum number of updates to retrieve. Defaults to 100.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start_polling(timeout, limit))

    def stop(self) -> None:
        """Stop the client."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.stop_polling())

    async def handle_webhook_update(self, update_data: Dict[str, Any]) -> None:
        """Process an update received via webhook.

        Args:
            update_data (Dict[str, Any]): Update data received from webhook
        """
        await self.process_update(update_data)
