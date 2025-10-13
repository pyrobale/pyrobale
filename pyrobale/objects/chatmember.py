from typing import TYPE_CHECKING
from typing import Optional, Union, Any

if TYPE_CHECKING:
    from .utils import build_api_url
    from .user import User
    from ..client import Client
from .chat import Chat
from .user import User
from .enums import ChatType


class ChatMember:
    """Represents a chat member in the Bale messenger, including their user
    information and status."""

    def __init__(
        self,
        user: "User",
        status: str,
        custom_title: Optional[str] = None,
        is_anonymous: Optional[bool] = None,
        can_be_edited: Optional[bool] = None,
        can_manage_chat: Optional[bool] = None,
        can_delete_messages: Optional[bool] = None,
        can_edit_messages: Optional[bool] = None,
        can_post_messages: Optional[bool] = None,
        can_restrict_members: Optional[bool] = None,
        can_promote_members: Optional[bool] = None,
        can_change_info: Optional[bool] = None,
        can_invite_users: Optional[bool] = None,
        can_pin_messages: Optional[bool] = None,
        can_manage_topics: Optional[bool] = None,
        until_date: Optional[int] = None,
        is_member: Optional[bool] = None,
        can_send_messages: Optional[bool] = None,
        can_send_audios: Optional[bool] = None,
        can_send_documents: Optional[bool] = None,
        can_send_photos: Optional[bool] = None,
        can_send_videos: Optional[bool] = None,
        can_send_video_notes: Optional[bool] = None,
        can_send_voice_notes: Optional[bool] = None,
        can_send_polls: Optional[bool] = None,
        can_send_other_messages: Optional[bool] = None,
        can_add_web_page_previews: Optional[bool] = None,
        chat: "Chat" = None,
        client: "Client" = None,
        **kwargs
    ):
        if isinstance(user, User):
            self.user = user
        else:
            self.user = User(**user)
        self.status = status
        self.custom_title = custom_title
        self.is_anonymous = is_anonymous
        self.can_be_edited = can_be_edited
        self.can_manage_chat = can_manage_chat
        self.can_delete_messages = can_delete_messages
        self.can_edit_messages = can_edit_messages
        self.can_post_messages = can_post_messages
        self.can_restrict_members = can_restrict_members
        self.can_promote_members = can_promote_members
        self.can_change_info = can_change_info
        self.can_invite_users = can_invite_users
        self.can_pin_messages = can_pin_messages
        self.can_manage_topics = can_manage_topics
        self.until_date = until_date
        self.is_member = is_member
        self.can_send_messages = can_send_messages
        self.can_send_audios = can_send_audios
        self.can_send_documents = can_send_documents
        self.can_send_photos = can_send_photos
        self.can_send_videos = can_send_videos
        self.can_send_video_notes = can_send_video_notes
        self.can_send_voice_notes = can_send_voice_notes
        self.can_send_polls = can_send_polls
        self.can_send_other_messages = can_send_other_messages
        self.can_add_web_page_previews = can_add_web_page_previews

        if client:
            self.client: Client = client
        else:
            self.client = kwargs.get("client")

        self.chat: Chat = chat

        if chat:
            self.chat: "Chat" = chat
        else:
            self.chat = kwargs.get("client")

        self.inputs = {k: v for k, v in {
            "can_be_edited": can_be_edited,
            "can_manage_chat": can_manage_chat,
            "can_delete_messages": can_delete_messages,
            "can_edit_messages": can_edit_messages,
            "can_post_messages": can_post_messages,
            "can_restrict_members": can_restrict_members,
            "can_promote_members": can_promote_members,
            "can_change_info": can_change_info,
            "can_invite_users": can_invite_users,
            "can_pin_messages": can_pin_messages,
            "can_manage_topics": can_manage_topics,
            "can_send_messages": can_send_messages,
            "can_send_audios": can_send_audios,
            "can_send_documents": can_send_documents,
            "can_send_photos": can_send_photos,
            "can_send_videos": can_send_videos,
            "can_send_video_notes": can_send_video_notes,
            "can_send_voice_notes": can_send_voice_notes,
            "can_send_polls": can_send_polls,
            "can_send_other_messages": can_send_other_messages,
            "can_add_web_page_previews": can_add_web_page_previews,
        }.items() if v is not None}

    async def ban(self) -> bool:
        """Bans the chat member from the chat.

        :param chat_id: The ID of the chat.
        :return: True if the member was banned successfully, False
            otherwise.
        """
        data = await self.chat.ban(self.user.id)
        return data

    async def kick(self) -> bool:
        """Kicks the chat member from the chat.

        :param chat_id: The ID of the chat.
        :return: True if the member was kicked successfully, False
            otherwise.
        """
        data = await self.chat.ban(self.user.id)
        data = await self.chat.unban(self.user.id)
        return data

    async def is_admin(self) -> bool:
        """Checks if the user is an administrator.

        :return: True if the user is an administrator.
        """
        if self.status in ['creator', 'administrator']:
            return True
        else:
            return False

    async def unban(self) -> bool:
        """Unbans the chat member from the chat.

        :return: True if the member was unbanned successfully, False
            otherwise.
        """
        data = await self.chat.unban(self.user.id)
        return data

    async def promote(
        self,
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
        return await self.chat.promote(
            chat_id=self.chat.id,
            user_id=self.user.id,
            can_change_info=can_change_info,
            can_post_messages=can_post_messages,
            can_edit_messages=can_edit_messages,
            can_delete_messages=can_delete_messages,
            can_invite_users=can_invite_users,
            can_restrict_members=can_restrict_members,
            can_pin_messages=can_pin_messages,
            can_promote_members=can_promote_members,
        )

    async def restrict(
        self,
        can_send_messages: Optional[bool] = None,
        can_send_media_messages: Optional[bool] = None,
        can_send_other_messages: Optional[bool] = None,
        can_add_web_page_previews: Optional[bool] = None,
        until_date: Optional[int] = None,
    ) -> bool:
        """Restrict a user in a chat.

        Parameters:
            can_send_messages (Optional[bool]): Pass True if the user can send text messages
            can_send_media_messages (Optional[bool]): Pass True if the user can send media messages
            can_send_other_messages (Optional[bool]): Pass True if the user can send other types of messages
            can_add_web_page_previews (Optional[bool]): Pass True if the user can add web page previews
            until_date (Optional[int]): Date when restrictions will be lifted for the user

        Returns:
            bool: True on success
        """
        return await self.chat.restrict(
            user_id=self.user.id,
            can_send_messages=can_send_messages,
            can_send_media_messages=can_send_media_messages,
            can_send_other_messages=can_send_other_messages,
            can_add_web_page_previews=can_add_web_page_previews,
            until_date=until_date,
        )
