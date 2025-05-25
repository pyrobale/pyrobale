from typing import TYPE_CHECKING
from typing import Optional, Union
if TYPE_CHECKING:
    from .utils import build_api_url
    from .user import User

class ChatMember:
    """
    Represents a chat member in the Bale messenger, including their user information and status.
    """
    def __init__(
                self,
                user: 'User',
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
                **kwargs
             ):
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
