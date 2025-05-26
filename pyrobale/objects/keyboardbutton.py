from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .webappinfo import WebAppInfo


class KeyboardButton:
    def __init__(
        self,
        text: str,
        request_contact: bool = False,
        request_location: bool = False,
        web_app: "WebAppInfo" = None,
        **kwargs
    ):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
        self.web_app = web_app
