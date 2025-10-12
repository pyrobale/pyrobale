from enum import Enum


class UpdatesTypes(Enum):
    """Types of updates."""

    MESSAGE = "message"
    MESSAGE_EDITED = "message_edited"
    CALLBACK_QUERY = "callback_query"
    PRE_CHECKOUT_QUERY = "pre_checkout_query"
    MEMBER_JOINED = "member_joined"
    MEMBER_LEFT = "member_left"
    SUCCESSFUL_PAYMENT = "successful_payment"
    COMMAND = "command"
    PHOTO = "photo"


class ChatPermissions(Enum):
    """permissions every user has in chats"""

    CAN_SEND_MESSAGE = "can_send_messages"
    CAN_SEND_MEDIA = "can_send_media_messages"
    CAN_SEND_AUDIO = "can_send_audios"
    CAN_SEND_DOCUMENT = "can_send_documents"
    CAN_SEND_PHOTOS = "can_send_photos"
    CAN_SEND_VIDEOS = "can_send_videos"
    CAN_SEND_POLLS = "can_send_polls"
    CAN_CHANGE_INFO = "can_change_info"
    CAN_INVITE_USERS = "can_invite_users"
    CAN_PIN_MESSAGE = "can_pin_messages"
    CAN_MANAGE_CHAT = "can_manage_chat"
    CAN_DELETE_MESSAGES = "can_delete_messages"
    CAN_RESTRICT_USERS = "can_restrict_members"
    CAN_PROMOTE_USERS = "can_promote_members"


class ChatAction(Enum):
    """Actions of a user in a chat."""

    TYPING = "typing"
    PHOTO = "upload_photo"
    VIDEO = "upload_video"
    REVORDVIDEO = "record_video"
    VOICE = "upload_voice"
    DOCUMENT = "upload_document"


class ChatType(Enum):
    """Types of chats."""

    PRIVATE = "private"
    GROUP = "group"
    CHANNEL = "channel"
