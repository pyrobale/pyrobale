from typing import TYPE_CHECKING, Union

from pyrobale.exceptions.common import PyroBaleException

if TYPE_CHECKING:
    from .webappinfo import WebAppInfo
    from .copytextbutton import CopyTextButton

from .enums import KeyboardTypes


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

    def __init__(self, *args):
        args = list(args)
        self.keyboard = []


        for i, row in enumerate(args):
            self.add_row()
            for i2, item in enumerate(row):
                item = list(item)
                if len(item) <= 0:
                    raise PyroBaleException(f"You cannot have a row with lower than 1 items! ({i}, {i2})")

                elif len(item) == 2:
                    if isinstance(item[1], KeyboardTypes):
                        item[1] = item[1].value
                    if item[1] in ["text", "request_contact", "request_location"]:
                        item_1 = item[1]
                        if item_1 == "text":
                            self.add_button(item[0])
                        elif item_1 == "request_contact":
                            self.add_button(item[0],request_contact=True)
                        else:
                            self.add_button(item[0],request_location=True)

                    elif isinstance(item[1], WebAppInfo) or (isinstance(item[1], str) and item[1].startswith("https://")):
                        self.add_button(item[0], web_app=item[1])

                    else:
                        raise PyroBaleException(f"You cannot have a button with type {item[1]}")
                else:
                    raise PyroBaleException("length of your item should not be more than two!")
                

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

    def to_dict(self):
        """Convert to a dictionary."""
        return {
            "keyboard": self.keyboard,
        }

    @property
    def json(self):
        return {"keyboard": self.keyboard}

    def __str__(self):
        return str(self.json)
