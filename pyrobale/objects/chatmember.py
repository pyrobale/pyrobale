from typing import TYPE_CHECKING
from typing import Optional, Union
if TYPE_CHECKING:
    from .utils import build_api_url
    from .user import User

class ChatMember:
    """
    Represents a chat member in the Bale messenger, including their user information and status.
    """
    def __init__(self, user: 'User', status: str, custom_title: str = None,
                 is_anonymous: bool = None, can_be_edited: bool = None,
                 can_manage_chat: bool = None, can_delete_messages: bool = None,
                 can_edit_messages: bool = None, can_post_messages: bool = None,
                 can_restrict_members: bool = None, can_promote_members: bool = None,
                 can_change_info: bool = None, can_invite_users: bool = None,
                 can_pin_messages: bool = None, can_manage_topics: bool = None,
                 until_date: int = None, is_member: bool = None,
                 can_send_messages: bool = None, can_send_audios: bool = None,
                 can_send_documents: bool = None, can_send_photos: bool = None,
                 can_send_videos: bool = None, can_send_video_notes: bool = None,
                 can_send_voice_notes: bool = None, can_send_polls: bool = None,
                 can_send_other_messages: bool = None, can_add_web_page_previews: bool = None):
        self.user = user
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
