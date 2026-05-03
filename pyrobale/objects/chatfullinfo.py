from typing import TYPE_CHECKING
from typing import Optional, Union

from pyrobale.exceptions.common import PyroBaleException
from .utils import smart_method
from .enums import ChatAction, ChatType

if TYPE_CHECKING:
    from .chatphoto import ChatPhoto
    from ..client import Client
    from .message import Message
    from .chatmember import ChatMember
    from ..objects.inlinekeyboardmarkup import InlineKeyboardMarkup
    from ..objects.replykeyboardmarkup import ReplyKeyboardMarkup

class ChatFullInfo:
    """Represents full info of a chat, usually returns in `get_chat`
    
    Parameters:
        id (int): Unique id of the chat.
        type (String or enums.ChatType): The type of the chat that can be private, group or channel.
        title (Optional[Str]): The title of chat in groups and channels.
        username (Optional[Str]): The username of chat (if exists).
        first_name (Optional[Str]): The first name of user in a private chat.
        last_name (Optional[Str]): The last name of user in a private chat.
        photo (Optional[ChatPhoto]): The photo of chat or the profile of the user. (if exists)
        bio (Optional[Str]): The biography of user. (if exists)
        description (Optional[Str]): The description of chat. (if exists)
        invite_link (Optional[Str]): The invite link of chat or channel. (if the bot has permission to make one)
        linked_chat_id (Optional[Str]): The chat id of the linked comment group to a channel. (if exists)
        **kwargs: Additional keyword arguments
    
    Attributes:
        id (int): Unique id of the chat.
        type (ChatType): The type of the chat that can be private, group or channel.
        title (Str): The title of chat in groups and channels.
        username (Str): The username of chat (if exists).
        first_name (Str): The first name of user in a private chat.
        last_name (Str): The last name of user in a private chat.
        full_name (Str): The property that returns the first_name and last_name together
        photo (ChatPhoto): The photo of chat or the profile of the user. (if exists)
        bio (Str): The biography of user. (if exists)
        description (Str): The description of chat. (if exists)
        invite_link (Str): The invite link of chat or channel. (if the bot has permission to make one)
        linked_chat_id (Str): The chat id of the linked comment group to a channel. (if exists)
        client (Client): Client instance
    """

    def __init__(self,
        id: int,
        type: Union[str, ChatType],
        title: Optional[str] = None,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        photo: Optional["ChatPhoto"] = None,
        bio: Optional[str] = None,
        description: Optional[str] = None,
        invite_link: Optional[str] = None,
        linked_chat_id: Optional[str] = None,
        client: Optional["Client"] = None
    ):
        self.id = id
        if isinstance(type, str):
            self.type = ChatType(type)
        else:
            self.type = type
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.photo: Optional["ChatPhoto"] = photo
        self.bio = bio
        self.description = description
        self.invite_link = invite_link
        self.linked_chat_id = linked_chat_id
        self.client: Optional["Client"] = client

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + self.last_name
    
    @property
    def is_private(self):
        return self.type == ChatType.PRIVATE
    
    @property
    def is_group(self):
        return self.type == ChatType.GROUP
    
    @property
    def is_channel(self):
        return self.type == ChatType.CHANNEL
    
    @property
    def has_linked_group(self):
        return bool(self.linked_chat_id)
    
    @smart_method
    async def send_message(
            self,
            text: str,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"]] = None,
    ) -> "Message":
        """Send a message to the chat.

        Parameters:
            text (str): Text of the message to be sent
            reply_to_message_id (int, optional): If the message is a reply, ID of the original message
            reply_markup (Union[ReplyKeyboardMarkup, InlineKeyboardMarkup], optional): Additional interface options

        Returns:
            Message: The sent message object
        """
        if isinstance(self.client, Client):
            return await self.client.send_message(
            chat_id=self.id,
            text=text,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup
        )
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def get_chat_member(self, user_id: int) -> "ChatMember":
        """Get information about a member of a chat.

        Parameters:
            user_id (int): Unique identifier of the target user

        Returns:
            ChatMember: Information about the chat member
        """
        if isinstance(self.client, Client):
            return await self.client.get_chat_member(chat_id=self.id, user_id=user_id)
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def get_administrators(self):
        """Gets a list of administrators of a specified chat.

        Returns:
            A list of administrators.
        """
        if isinstance(self.client, Client):
            return await self.client.get_chat_administrators(self.id)
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def get_chat_members_count(self) -> int:
        """Get the number of members in the chat.

        Returns:
            int: Number of members in the chat
        """
        if isinstance(self.client, Client):
            return await self.client.get_chat_members_count(chat_id=self.id)
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def send_photo(
            self,
            photo: str,
            caption: Optional[str] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"]] = None,
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
        if isinstance(self.client, Client):
            return await self.client.send_photo(
            chat_id=self.id,
            photo=photo,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def send_video(
            self,
            video: str,
            caption: Optional[str] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"]] = None,
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
        if isinstance(self.client, Client):
            return await self.client.send_video(
            chat_id=self.id,
            video=video,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def send_audio(
            self,
            audio: str,
            caption: Optional[str] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"]] = None,
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
        if isinstance(self.client, Client):
            return await self.client.send_audio(
            chat_id=self.id,
            audio=audio,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def send_document(
            self,
            document: str,
            caption: Optional[str] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"]] = None,
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
        if isinstance(self.client, Client):
            return await self.client.send_document(
            chat_id=self.id,
            document=document,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def send_sticker(
            self,
            sticker: str,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"]] = None,
    ) -> "Message":
        """Send a sticker to the chat.

        Parameters:
            sticker (str): Sticker to send (file_id or URL)
            reply_to_message_id (int, optional): If the message is a reply, ID of the original message
            reply_markup (Union[ReplyKeyboardMarkup, InlineKeyboardMarkup], optional): Additional interface options

        Returns:
            Message: The sent message object
        """
        if isinstance(self.client, Client):
            return await self.client.send_sticker(
            chat_id=self.id,
            sticker=sticker,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def send_voice(
            self,
            voice: str,
            caption: Optional[str] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"]] = None,
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
        if isinstance(self.client, Client):
            return await self.client.send_voice(
            chat_id=self.id,
            voice=voice,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def send_location(
            self,
            latitude: float,
            longitude: float,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"]] = None,
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
        if isinstance(self.client, Client):
            return await self.client.send_location(
            chat_id=self.id,
            latitude=latitude,
            longitude=longitude,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def send_contact(
            self,
            phone_number: str,
            first_name: str,
            last_name: Optional[str] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"]] = None,
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
        if isinstance(self.client, Client):
            return await self.client.send_contact(
            chat_id=self.id,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def ban(self, user_id: int) -> bool:
        """Bans a user from the chat.

        Parameters:
            user_id (int): Unique identifier of the target user
            until_date (Optional[int]): Date when the user will be unbanned (Unix time)

        Returns:
            bool: True on success
        """
        if isinstance(self.client, Client):
            return await self.client.ban_chat_member(chat_id=self.id, user_id=user_id)
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def kick(self, user_id: int) -> bool:
        """Kicks a user from the chat.

        Parameters:
            user_id (int): Unique identifier of the target user

        Returns:
            bool: True on success
        """
        if isinstance(self.client, Client):
            return await self.client.kick_chat_member(chat_id=self.id, user_id=user_id)
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def unban(self, user_id: int) -> bool:
        """Unban a previously banned user in the chat.

        Parameters:
            user_id (int): Unique identifier of the target user

        Returns:
            bool: True on success
        """
        if isinstance(self.client, Client):
            return await self.client.unban_chat_member(chat_id=self.id, user_id=user_id)
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def restrict(self,
                       user_id: int,
                       can_send_messages: Union[bool, None] = None,
                       can_send_media_messages: Union[bool, None] = None,
                       can_send_other_messages: Union[bool, None] = None,
                       can_add_web_page_previews: Union[bool, None] = None,
                       until_date: Union[int, None] = None
                       ) -> bool:
        """Restricts a user from a chat.

        Args:
            user_id (int): The user to ban.
            can_send_messages (Union[bool,None]): Default is None
            can_send_media_messages (Union[bool,None]): Default is None
            can_send_other_messages (Union[bool,None]): Default is None
            can_add_web_page_previews (Union[bool,None]): Default is None
            until_date: (Union[int,None]) Default is None

        Returns:
            bool: Whether the ban was successful.
        """
        if isinstance(self.client, Client):
            return await self.client.restrict_chat_member(
            chat_id=self.id,
            user_id=user_id,
            can_send_messages=can_send_messages,
            can_send_media_messages=can_send_media_messages,
            can_send_other_messages=can_send_other_messages,
            can_add_web_page_previews=can_add_web_page_previews,
            until_date=until_date
        )
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
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
    ) -> bool:
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
        if isinstance(self.client, Client):
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
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def leave(self) -> bool:
        """Leave the chat.

        Returns:
            bool: True on success
        """
        if isinstance(self.client, Client):
            return await self.client.leave_chat(chat_id=self.id)
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def delete_message(self, message_id: int) -> bool:
        """Delete a message in a chat.

        Args:
            message_id (int): Unique identifier of the target message
        Returns:
            bool: True on success
        """

        if isinstance(self.client, Client):
            return await self.client.delete_message(chat_id=self.id, message_id=message_id)
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def edit_message(self, message_id: int, text: str, reply_markup: Optional[Union["InlineKeyboardMarkup", "ReplyKeyboardMarkup"]] = None):
        """Edit a message in a chat.

        Args:
            message_id (int): Unique identifier of the target message
            text (str): Text to edit.
            reply_markup (Optional[InlineKeyboardMarkup, ReplyKeyboardMarkup]): Optional inline keyboard.

        Returns:
            Message: The edited message.
        """
        if isinstance(self.client, Client):
            return await self.client.edit_message(chat_id=self.id, message_id=message_id, text=text, reply_markup=reply_markup)
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def edit_message_reply_markup(self, message_id: int, reply_markup: Union["InlineKeyboardMarkup", None]) -> "Message":
        """Edit a message's reply markup without editing content.

        Args:
            message_id (int): Unique identifier of the target message.
            reply_markup (Union["InlineKeyboardMarkup", None]): Reply markup without editing content.
        Returns:
            Message: The edited message.
        """

        if isinstance(self.client, Client):
            return await self.client.edit_message_reply_markup(
            chat_id=self.id,
            message_id=message_id,
            reply_markup=reply_markup
        )
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def is_joined(self, user_id: int) -> bool:
        """Check if a user is joined to the chat.

        Parameters:
            user_id (int): Unique identifier of the target user

        Returns:
            bool: True if the user is joined to the chat, False otherwise
        """
        if isinstance(self.client, Client):
            return await self.client.is_joined(user_id, self.id)
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def pin(self, message_id: int) -> bool:
        """Pin a message in the chat.

        Parameters:
            message_id (int): Identifier of a message to pin

        Returns:
            bool: True on success
        """
        if isinstance(self.client, Client):
            return await self.client.pin_chat_message(
            chat_id=self.id, message_id=message_id
        )
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def unpin(self, message_id: int) -> bool:
        """Unpin a message in the chat.

        Returns:
            bool: True on success
        """
        if isinstance(self.client, Client):
            return await self.client.unpin_chat_message(chat_id=self.id, message_id=message_id)
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def unpin_all(self) -> bool:
        """Unpin all messages in the chat.

        Returns:
            bool: True on success
        """
        if isinstance(self.client, Client):
            return await self.client.unpin_all_chat_messages(chat_id=self.id)
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def set_title(self, title: str) -> bool:
        """Change the title of a chat.

        Parameters:
            title (str): New chat title, 1-255 characters

        Returns:
            bool: True on success
        """
        if isinstance(self.client, Client):
            return await self.client.set_chat_title(chat_id=self.id, title=title)
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def set_description(self, description: str) -> bool:
        """Change the description of a chat.

        Parameters:
            description (str): New chat description, 0-255 characters

        Returns:
            bool: True on success
        """
        if isinstance(self.client, Client):
            return await self.client.set_chat_description(
            chat_id=self.id, description=description
        )
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def set_photo(self, photo: str) -> bool:
        """Set the photo of the chat.

        Parameters:
            photo (str): Photo to set. Pass a file_id as string to send a photo that exists on the Telegram servers, pass an HTTP URL as a string for Telegram to get a photo from the Internet, or pass "attach://<file_attach_name>" to upload a new photo that exists on the local server.

        Returns:
            bool: True on success
        """
        if isinstance(self.client, Client):
            return await self.client.set_chat_photo(chat_id=self.id, photo=photo)
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def send_action(self, action: ChatAction) -> bool:
        """Send an action to the chat.

        Parameters:
            action (objects.enums.ChatAction): Action to send to the chat

        Returns:
            bool: True on success
        """
        if isinstance(self.client, Client):
            return await self.client.send_chat_action(chat_id=self.id, action=action)
        else:
            raise PyroBaleException("You cannot use client functions without a valid client object")
    @smart_method
    async def mute(self, user_id: int) -> bool:
        """
        Mutes a user in a chat by restricting.

        Parameters:
            user_id (int): user id to mute

        Returns:
            bool: True on success
        """
        return await self.restrict(user_id=user_id, can_send_messages=False)

    @smart_method
    async def unmute(self, user_id: int) -> bool:
        """
        Unmutes a user in a chat by restricting.

        Parameters:
            user_id (int): user id to unmute

        Returns:
            bool: True on success
        """
        return await self.restrict(user_id=user_id, can_send_messages=True)
