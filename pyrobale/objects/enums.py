from enum import Enum

class UpdatesTypes(Enum):
    MESSAGE = "message"
    MESSAGE_EDITED = "message_edited"
    CALLBACK_QUERY = "callback_query"
    PRE_CHECKOUT_QUERY = "pre_checkout_query"
    MEMBER_JOINED = "member_joined"
    MEMBER_LEFT = "member_left"

class ChatAction(Enum):
    TYPING = "typing"
    PHOTO = "upload_photo"
    VIDEO = "upload_video"

class ChatType(Enum):
    PRIVATE = "private"
    GROUP = "group"
    CHANNEL = "channel"