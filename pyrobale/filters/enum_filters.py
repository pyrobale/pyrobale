from enum import Enum

class Filters(Enum):
    """Filters that you can use in handlers"""

    TEXT = "text"
    PHOTO = "photo"
    VIDEO = "video"
    AUDIO = "audio"
    VOICE = "voice"
    CONTACT = "contact"
    LOCATION = "location"