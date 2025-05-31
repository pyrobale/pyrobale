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
    COMMAND = "message"





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
