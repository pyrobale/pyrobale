from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .message import Message
    from .callbackquery import CallbackQuery
    from .precheckoutquery import PreCheckoutQuery


class Update:
    def __init__(
        self,
        update_id: int,
        message: Optional["Message"] = None,
        edited_message: Optional["Message"] = None,
        callback_query: Optional["CallbackQuery"] = None,
        pre_checkout_query: Optional["PreCheckoutQuery"] = None,
        **kwargs
    ):
        self.update_id = update_id
        self.message = message
        self.edited_message = edited_message
        self.callback_query = callback_query
        self.pre_checkout_query = pre_checkout_query
