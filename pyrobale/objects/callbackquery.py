from typing import Optional


class CallbackQuery:
    """Represents a callback query from a user."""

    def __init__(
        self,
        id: Optional[str] = None,
        user: Optional[dict] = None,
        message: Optional[dict] = None,
        data: Optional[str] = None,
        **kwargs
    ):
        self.id = id
        self.user = None
        self.message = None
        self.chat = None
        self.data = data if data else None
        self.bot = kwargs.get("kwargs", {}).get("client", None)

        if user:
            from .user import User

            self.user = User(**user)

        if message:
            from .message import Message

            self.message = Message(**message)
            self.chat = self.message.chat if self.message else None

    async def answer(
        self, text: Optional[str] = None, show_alert: bool = False
    ) -> bool:
        """Sends a response to the callback query."""
        return await self.bot.answer_callback_query(self.id, text, show_alert)
