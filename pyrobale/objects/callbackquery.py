import typing
from typing import Optional, Union
from .utils import smart_method
from .inlinekeyboardmarkup import InlineKeyboardMarkup
from .replykeyboardmarkup import ReplyKeyboardMarkup

if typing.TYPE_CHECKING:
    from ..client import Client

class CallbackQuery:
    """Represents a callback query from a user."""

    def __init__(
        self,
        id: Optional[str] = None,
        from_user: Optional[dict] = None,
        message: Optional[dict] = None,
        data: Optional[str] = None,
        **kwargs
    ):
        self.id = id
        self.user = None
        self.message = None
        self.chat = None
        self.data = data if data else None
        self.bot: Client = kwargs.get("client", None)

        if from_user:
            from .user import User

            self.user = User(**from_user)

        if message:
            from .message import Message

            self.message = Message(**message)
            self.chat = self.message.chat if self.message else None

    @smart_method
    async def answer(
        self, text: Optional[str] = None, show_alert: bool = False
    ) -> bool:
        """Sends a response to the callback query."""
        return await self.bot.answer_callback_query(self.id, text, show_alert)
    
    @smart_method
    async def reply(self,
            text: str,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None):
        """Sends a message to the author of callback query"""
        return await self.bot.send_message(self.user.id, text, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)
    
    @property
    def is_answerable(self):
        return self.data.startswith("1")
