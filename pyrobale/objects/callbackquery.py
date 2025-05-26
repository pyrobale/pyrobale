from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from .user import User
    from .message import Message
    from ..client import Client

from .user import User
from .message import Message
from .chat import Chat

class CallbackQuery:
    """
    Represents a callback query from a user.
    """
    def __init__(self,
                id: Optional[str] = None,
                user: Optional['User'] = None,
                message: Optional['Message'] = None,
                data: Optional[str] = None,
                **kwargs
                ):
        self.id = id
        self.user : 'User' = User(**user) if user else None
        self.message : 'Message' = Message(**message) if message else None
        self.chat : 'Chat' = self.message.chat if self.message else None
        self.data = data if data else None
        self.bot : 'Client' = kwargs.get('kwargs',{}).get('client', None)
    
    async def answer(self, text: Optional[str] = None, show_alert: bool = False):
        """
        Sends a response to the callback query.
        """
        return await self.bot.answer_callback_query(self.id, text, show_alert)