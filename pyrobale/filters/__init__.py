import re
from enum import Enum
from typing import List, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ..objects.user import User
    from ..client import Client

def equals(expected_text: str):
    """
    Check if the event text or caption or callbackQuery data is equal to the expected text.
    
    Args:
        expected_text (str): The expected text to compare with.

    Returns:
        Callable: A function that checks if the event text or caption or callbackQuery data is equal to the expected text.
    """
    def check(event, *args):
        try:
            return getattr(event, "text", None) == expected_text or getattr(event, "caption", None) == expected_text or getattr(event, "data", None) == expected_text
        except:
            return False
    return check

def startswith(expected_text: str):
    """
    Check if the event text or caption or callbackQuery data is started with to the expected text.
    
    Args:
        expected_text (str): The expected text to compare with.

    Returns:
        Callable: A function that checks if the event text or caption or callbackQuery data is started with to the expected text.
    """
    def check(event, *args):
        try:
            return getattr(event, "text", "").startswith(expected_text) or getattr(event, "caption", "").startswith(expected_text) or getattr(event, "data", "").startswith(expected_text)
        except:
            return False
    return check


def regex(pattern: str):
    """
    checks the event text or caption with given pattern using regex
    
    Args:
        pattern (str): The pattern to check with text
    
    Returns:
        Callable: A function that checks if the event text or caption is match with given pattern
    """
    def check(event, *args):
        try:
            return re.search(pattern, getattr(event, "text", "")) or re.search(pattern, getattr(event, "caption", ""))
        except:
            return False
    return check

def from_users(allowed_users: Union[List[Union["User", int, str]], int, str]):
    """
    Check if the event text or caption or callbackQuery sender is in allowed user.
    
    Args:
        allowed_users (List[Union["User", int]]): Allowed users to use this handler.

    Returns:
        Callable: A function that checks if the event text or caption or callbackQuery sender is in allowed user.
    """
    if type(allowed_users) in [str, int]:
        try:
            allowed_users = [int(allowed_users)]
        except:
            raise ValueError("Chat IDs can only be digits")
    def check(event, *args):
        try:
            event_user = getattr(event, "user", None)
            event_user_id = getattr(event_user, "id")
            if event_user_id in allowed_users:
                return True
        except:
            return False
    return check

def is_joined(chat_ids: Union[List[Union["User", int, str]], int, str]):
    """
    Check if the event text or caption or callbackQuery sender is in allowed user.
    
    Args:
        allowed_users (List[Union["User", int]]): Allowed users to use this handler.

    Returns:
        Callable: A function that checks if the event text or caption or callbackQuery sender is in allowed user.
    """
    if type(chat_ids) in [str, int]:
        try:
            chat_ids = [int(chat_ids)]
        except:
            raise ValueError("Chat IDs can only be digits")

    def check(event, client: 'Client', *args):
        try:
            event_user = getattr(event, "user", None)
            event_user_id = getattr(event_user, "id")
            for chat in chat_ids:
                joined = client.is_joined(event_user_id, chat)
                if not joined:
                    return False
            return True
            
        except:
            return False
    return check

def _private():
    """
    checks if the event is happening in a private chat
    """

    def check(event, *args):
        try:
            chat = getattr(event, "chat")
            return getattr(chat, "private")
        except:
            return False
    return check

def _group():
    """
    checks if the event is happening in a group chat
    """

    def check(event, *args):
        try:
            chat = getattr(event, "chat")
            type = getattr(chat, "type")
            return type == "group"
        except:
            return False
    return check

def _digit():
    """
    Check if the event text or caption or callbackQuery data is digit.
    
    Returns:
        Callable: A function that checks if the event text or caption or callbackQuery data is digit.
    """
    def check(event, *args):
        try:
            return getattr(event, "text", "").isdigit() or getattr(event, "caption", "").isdigit() or getattr(event, "data", "").isdigit()
        except:
            return False
    return check

def _channel():
    """
    checks if the event is happening in a channel
    """

    def check(event, args):
        try:
            chat = getattr(event, "chat")
            return getattr(chat, "channel")
        except:
            return False
    return check

text = TEXT = "text"
photo = PHOTO = "photo"
video = VIDEO = "video"
audio = AUDIO = "audio"
voice = VOICE = "voice"
contact = CONTACT = "contact"
location = LOCATION = "location"

private = pv = _private()
channel = _channel()
group = _group()
digit = _digit()