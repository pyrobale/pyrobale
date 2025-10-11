from typing import TYPE_CHECKING
from typing import Optional, Union

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



class Chat:
    """Represents a chat in the Bale messenger.

    Parameters:
        id (Optional[int]): Unique identifier for this chat
        type (Optional[str]): Type of chat, can be either "private", "group", or "channel"
        title (Optional[str]): Title, for groups and channels
        username (Optional[str]): Username, for private chats and channels if available
        first_name (Optional[str]): First name of the other party in a private chat
        last_name (Optional[str]): Last name of the other party in a private chat
        photo (Optional[ChatPhoto]): Chat photo object
        **kwargs: Additional keyword arguments

    Attributes:
        id (int): Unique identifier for this chat
        type (str): Type of chat
        PRIVATE (bool): True if chat is private
        GROUP (bool): True if chat is group
        CHANNEL (bool): True if chat is channel
        title (str): Chat title
        username (str): Chat username
        first_name (str): First name
        last_name (str): Last name
        photo (ChatPhoto): Chat photo
        client (Client): Client instance
    """

    def __init__(
        self,
        id: Optional[int] = None,
        type: Optional[str] = None,
        title: Optional[str] = None,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        photo: Optional["ChatPhoto"] = None,
        client: Optional["Client"] = None,
        **kwargs
    ):
        self.id = id
        self.type = type
        self.PRIVATE = self.type == "private"
        self.GROUP = self.type == "group"
        self.CHANNEL = self.type == "channel"
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.photo: "ChatPhoto" = photo
        self.client: "Client" = client

    async def send_message(
        self,
        text: str,
        reply_to_message_id: int = None,
        reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> "Message":
        """Send a message to the chat.

        Parameters:
            text (str): Text of the message to be sent
            reply_to_message_id (int, optional): If the message is a reply, ID of the original message
            reply_markup (Union[ReplyKeyboardMarkup, InlineKeyboardMarkup], optional): Additional interface options

        Returns:
            Message: The sent message object
        """
        self.client.send_message(
            chat_id=self.id,
            text=text,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )

    async def get_chat_member(self, user_id: int) -> "ChatMember":
        """Get information about a member of a chat.

        Parameters:
            user_id (int): Unique identifier of the target user

        Returns:
            ChatMember: Information about the chat member
        """
        return await self.client.get_chat_member(chat_id=self.id, user_id=user_id)

    async def get_chat_members_count(self) -> int:
        """Get the number of members in the chat.

        Returns:
            int: Number of members in the chat
        """
        return await self.client.get_chat_members_count(chat_id=self.id)

    async def send_photo(
        self,
        photo: str,
        caption: Optional[str] = None,
        reply_to_message_id: int = None,
        reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> "Message":
        """Send a photo to the chat.

        Parameters:
            photo (str): Photo to send (file_id or URL)
            caption (Optional[str]): Photo caption
            reply_to_message_id (int, optional): If the message is a reply, ID of the original message
            reply_markup (Union[ReplyKeyboardMarkup, InlineKeyboardMarkup], optional): Additional interface options

        Returns:
            Message: The sent message object
        """
        self.client.send_photo(
            chat_id=self.id,
            photo=photo,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )

    async def send_video(
        self,
        video: str,
        caption: Optional[str] = None,
        reply_to_message_id: int = None,
        reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> "Message":
        """Send a video to the chat.

        Parameters:
            video (str): Video to send (file_id or URL)
            caption (Optional[str]): Video caption
            reply_to_message_id (int, optional): If the message is a reply, ID of the original message
            reply_markup (Union[ReplyKeyboardMarkup, InlineKeyboardMarkup], optional): Additional interface options

        Returns:
            Message: The sent message object
        """
        self.client.send_video(
            chat_id=self.id,
            video=video,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )

    async def send_audio(
        self,
        audio: str,
        caption: Optional[str] = None,
        reply_to_message_id: int = None,
        reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> "Message":
        """Send an audio file to the chat.

        Parameters:
            audio (str): Audio file to send (file_id or URL)
            caption (Optional[str]): Audio caption
            reply_to_message_id (int, optional): If the message is a reply, ID of the original message
            reply_markup (Union[ReplyKeyboardMarkup, InlineKeyboardMarkup], optional): Additional interface options

        Returns:
            Message: The sent message object
        """
        self.client.send_audio(
            chat_id=self.id,
            audio=audio,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )

    async def send_document(
        self,
        document: str,
        caption: Optional[str] = None,
        reply_to_message_id: int = None,
        reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> "Message":
        """Send a document to the chat.

        Parameters:
            document (str): Document to send (file_id or URL)
            caption (Optional[str]): Document caption
            reply_to_message_id (int, optional): If the message is a reply, ID of the original message
            reply_markup (Union[ReplyKeyboardMarkup, InlineKeyboardMarkup], optional): Additional interface options

        Returns:
            Message: The sent message object
        """
        self.client.send_document(
            chat_id=self.id,
            document=document,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )

    async def send_sticker(
        self,
        sticker: str,
        reply_to_message_id: int = None,
        reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> "Message":
        """Send a sticker to the chat.

        Parameters:
            sticker (str): Sticker to send (file_id or URL)
            reply_to_message_id (int, optional): If the message is a reply, ID of the original message
            reply_markup (Union[ReplyKeyboardMarkup, InlineKeyboardMarkup], optional): Additional interface options

        Returns:
            Message: The sent message object
        """
        self.client.send_sticker(
            chat_id=self.id,
            sticker=sticker,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )

    async def send_voice(
        self,
        voice: str,
        caption: Optional[str] = None,
        reply_to_message_id: int = None,
        reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> "Message":
        """Send a voice message to the chat.

        Parameters:
            voice (str): Voice message to send (file_id or URL)
            caption (Optional[str]): Voice message caption
            reply_to_message_id (int, optional): If the message is a reply, ID of the original message
            reply_markup (Union[ReplyKeyboardMarkup, InlineKeyboardMarkup], optional): Additional interface options

        Returns:
            Message: The sent message object
        """
        self.client.send_voice(
            chat_id=self.id,
            voice=voice,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )

    async def send_location(
        self,
        latitude: float,
        longitude: float,
        reply_to_message_id: int = None,
        reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> "Message":
        """Send a location to the chat.

        Parameters:
            latitude (float): Latitude of the location
            longitude (float): Longitude of the location
            reply_to_message_id (int, optional): If the message is a reply, ID of the original message
            reply_markup (Union[ReplyKeyboardMarkup, InlineKeyboardMarkup], optional): Additional interface options

        Returns:
            Message: The sent message object
        """
        self.client.send_location(
            chat_id=self.id,
            latitude=latitude,
            longitude=longitude,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )

    async def send_contact(
        self,
        phone_number: str,
        first_name: str,
        last_name: Optional[str] = None,
        reply_to_message_id: int = None,
        reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> "Message":
        """Send a contact to the chat.

        Parameters:
            phone_number (str): Contact's phone number
            first_name (str): Contact's first name
            last_name (Optional[str]): Contact's last name
            reply_to_message_id (int, optional): If the message is a reply, ID of the original message
            reply_markup (Union[ReplyKeyboardMarkup, InlineKeyboardMarkup], optional): Additional interface options

        Returns:
            Message: The sent message object
        """
        self.client.send_contact(
            chat_id=self.id,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )

    async def ban(self, user_id: int) -> bool:
        """Bans a user from the chat.

        Parameters:
            user_id (int): Unique identifier of the target user
            until_date (Optional[int]): Date when the user will be unbanned (Unix time)

        Returns:
            bool: True on success
        """
        return await self.client.ban_chat_member(chat_id=self.id, user_id=user_id)

    async def kick(self, user_id: int) -> bool:
        """Kicks a user from the chat.

        Parameters:
            user_id (int): Unique identifier of the target user

        Returns:
            bool: True on success
        """
        return await self.client.kick_chat_member(chat_id=self.id, user_id=user_id)

    async def unban(self, user_id: int) -> bool:
        """Unban a previously banned user in the chat.

        Parameters:
            user_id (int): Unique identifier of the target user

        Returns:
            bool: True on success
        """
        return await self.client.unban_chat_member(chat_id=self.id, user_id=user_id)

    async def promote(
        self,
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
        """Promote or demote a user in a chat.

        Parameters:
            user_id (int): Unique identifier of the target user
            can_change_info (Optional[bool]): Pass True if the user can change chat title, photo and other settings
            can_post_messages (Optional[bool]): Pass True if the user can post messages in channels
            can_edit_messages (Optional[bool]): Pass True if the user can edit messages in channels
            can_delete_messages (Optional[bool]): Pass True if the user can delete messages
            can_invite_users (Optional[bool]): Pass True if the user can invite new users
            can_restrict_members (Optional[bool]): Pass True if the user can restrict, ban or unban chat members
            can_pin_messages (Optional[bool]): Pass True if the user can pin messages
            can_promote_members (Optional[bool]): Pass True if the user can add new administrators

        Returns:
            bool: True on success
        """
        return await self.client.promote_chat_member(
            chat_id=self.id,
            user_id=user_id,
            can_change_info=can_change_info,
            can_post_messages=can_post_messages,
            can_edit_messages=can_edit_messages,
            can_delete_messages=can_delete_messages,
            can_invite_users=can_invite_users,
            can_restrict_members=can_restrict_members,
            can_pin_messages=can_pin_messages,
            can_promote_members=can_promote_members,
        )

    async def leave(self) -> bool:
        """Leave the chat.

        Returns:
            bool: True on success
        """
        return await self.client.leave_chat(chat_id=self.id)
    
    async def is_joined(self, user_id: int) -> bool:
        """Check if a user is joined to the chat.
        
        Parameters:
            user_id (int): Unique identifier of the target user
        
        Returns:
            bool: True if the user is joined to the chat, False otherwise
        """
        return await self.client.is_joined(user_id, self.id)

    async def pin(self, message_id: int) -> bool:
        """Pin a message in the chat.

        Parameters:
            message_id (int): Identifier of a message to pin

        Returns:
            bool: True on success
        """
        return await self.client.pin_chat_message(
            chat_id=self.id, message_id=message_id
        )

    async def unpin(self) -> bool:
        """Unpin a message in the chat.

        Returns:
            bool: True on success
        """
        return await self.client.unpin_chat_message(chat_id=self.id)

    async def unpin_all(self) -> bool:
        """Unpin all messages in the chat.

        Returns:
            bool: True on success
        """
        return await self.client.unpin_all_chat_messages(chat_id=self.id)

    async def set_title(self, title: str) -> bool:
        """Change the title of a chat.

        Parameters:
            title (str): New chat title, 1-255 characters

        Returns:
            bool: True on success
        """
        return await self.client.set_chat_title(chat_id=self.id, title=title)

    async def set_description(self, description: str) -> bool:
        """Change the description of a chat.

        Parameters:
            description (str): New chat description, 0-255 characters

        Returns:
            bool: True on success
        """
        return await self.client.set_chat_description(
            chat_id=self.id, description=description
        )

    async def set_photo(self, photo: str) -> bool:
        """Set the photo of the chat.

        Parameters:
            photo (str): Photo to set. Pass a file_id as string to send a photo that exists on the Telegram servers, pass an HTTP URL as a string for Telegram to get a photo from the Internet, or pass "attach://<file_attach_name>" to upload a new photo that exists on the local server.

        Returns:
            bool: True on success
        """
        return await self.client.set_chat_photo(chat_id=self.id, photo=photo)

    async def send_action(self, action: ChatAction) -> bool:
        """Send an action to the chat.

        Parameters:
            action (objects.enums.ChatAction): Action to send to the chat

        Returns:
            bool: True on success
        """
        return await self.client.send_chat_action(chat_id=self.id, action=action)
