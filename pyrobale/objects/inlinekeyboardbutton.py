from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .webappdata import WebAppData
    from .copytextbutton import CopyTextButton


class InlineKeyboardButton:
    """Represents a button in an inline keyboard."""

    def __init__(
        self,
        text: str,
        url: str = None,
        callback_data: str = None,
        web_app: "WebAppData" = None,
        copy_text_button: "CopyTextButton" = None,
        **kwargs
    ):
        self.text = text
        self.url = url
        self.callback_data = callback_data
        self.web_app = web_app
        self.copy_text_button = copy_text_button
