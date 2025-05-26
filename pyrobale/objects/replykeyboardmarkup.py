from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .webappinfo import WebAppInfo
    from .copytextbutton import CopyTextButton


class ReplyKeyboardMarkup:
    """
    Represents a reply keyboard.
    Attributes:
        Each dictionary contains the following keys:
            - keyboard (list): A list of lists of dictionaries representing the buttons in the keyboard.
            - text (str): The text of the button.
            - request_contact (bool, optional): If True, the user's phone number will be sent.
            - request_location (bool, optional): If True, the user's location will be sent.
            - web_app (WebApp, optional): The web app associated with the button.
    """

    def __init__(self):
        self.keyboard = []

    def add_button(
        self,
        text: str,
        request_contact: bool = None,
        request_location: bool = None,
        web_app: Union["WebAppInfo", str] = None,
    ):
        """Add a button to the current row."""
        button = {"text": text}
        if request_contact:
            button["request_contact"] = request_contact
        if request_location:
            button["request_location"] = request_location
        if web_app:
            button["web_app"] = web_app

        if not self.keyboard:
            self.keyboard.append([])
        self.keyboard[-1].append(button)
        return self

    def add_row(self):
        """Add a new row for buttons."""
        self.keyboard.append([])
        return self

    @property
    def json(self):
        return {"keyboard": self.keyboard}

    def __str__(self):
        return str(self.json)
