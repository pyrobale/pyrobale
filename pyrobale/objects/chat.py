from typing import TYPE_CHECKING
from typing import Optional, Union
if TYPE_CHECKING:
    from .utils import build_api_url
    from .chatphoto import ChatPhoto
    from .message import Message
    from .user import User
    from .chatmember import ChatMember
import asyncio
import aiohttp

class Chat:
    """
    Represents a chat in the Bale messenger.
    """
    def __init__(self, id: int, type: str, title: Optional[str], username: Optional[str], first_name: Optional[str], last_name: Optional[str], photo: Optional['ChatPhoto']):
        self.id = id
        self.type = type
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.photo = photo