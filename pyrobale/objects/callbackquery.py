from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import User
    from .message import Message

class CallbackQuery:
    """
    Represents a callback query from a user.
    """
    def __init__(self, id: str, user: 'User', message: 'Message', data: str):
        self.id = id
        self.user = user
        self.message = message
        self.data = data