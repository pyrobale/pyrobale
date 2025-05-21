from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from .webappinfo import WebAppInfo
    from .copytextbutton import CopyTextButton

class InlineKeyboardMarkup:
    """
    Represents an inline keyboard.
    Attributes:
        Each dictionary contains the following keys:
            - inline_keyboard (list): A list of lists of dictionaries representing the buttons in the keyboard.
            - text (str): The text of the button.
            - callback_data (str, optional): The callback data associated with the button.
            - url (str, optional): The URL associated with the button.
            - web_app (WebApp, optional): The web app associated with the button.
            - copy_text_button (CopyTextButton, optional): The copy text button associated with the button.
    """
    def __init__(self):
        self.inline_keyboard = []

    def add_button(self, text: str, callback_data: str = None, url: str = None, web_app: Union['WebAppInfo',str] = None, copy_text_button: 'CopyTextButton' = None):
        """Add a button to the current row"""
        button = {"text": text}
        if callback_data:
            button["callback_data"] = callback_data
        if url:
            button["url"] = url
        if web_app:
            button["web_app"] = web_app
        if copy_text_button:
            button["copy_text_button"] = copy_text_button.text
        if not any(button.values()):
            raise ValueError("At least one attribute must be provided for the button")
        
        if [callback_data, url, web_app, copy_text_button].count(None) > 1:
            raise ValueError("Only one of callback_data, url, web_app, or copy_text_button can be provided for a button")
                
        if not self.inline_keyboard:
            self.inline_keyboard.append([])
        self.inline_keyboard[-1].append(button)
        return self
    
    def add_row(self):
        """Add a new row for buttons"""
        self.inline_keyboard.append([])
        return self
    
    @property
    def json(self):
        return {"inline_keyboard": self.inline_keyboard}
    
    def __str__(self):
        return str(self.json)