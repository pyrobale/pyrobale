import re
from typing import Callable, List, Optional, Union, TYPE_CHECKING
import asyncio

if TYPE_CHECKING:
    from ..objects.user import User
    from ..client import Client

class Filter:
    def __init__(self, check_func: Callable, inv: bool = False) -> None:
        self.state = (check_func, inv)
        self.lst = [self.state]

    def __invert__(self):
        self.state = (self.state[0], not self.state[1])
        self.lst = [self.state]
        return self

    def __and__(self, other):
        if not isinstance(other, Filter):
            raise TypeError(f"Cannot combine Filter with {type(other)}")

        def combined_check(event, client=None, *args):
            if self.state[1]:
                res1 = not self.state[0](event, client, *args)
            else:
                res1 = self.state[0](event, client, *args)

            if other.state[1]:
                res2 = not other.state[0](event, client, *args)
            else:
                res2 = other.state[0](event, client, *args)

            return res1 and res2

        new_filter = Filter(self.state[0], self.state[1])
        new_filter.lst = self.lst + other.lst
        new_filter.state = (combined_check, False)
        return new_filter

    def __call__(self, event, client=None, *args):
        if self.state[1]:
            return not self.state[0](event, client, *args)
        return self.state[0](event, client, *args)

def equals(expected_text: Union[str, List[str]]):
    """
    Check if the event text or caption or callbackQuery data is equal to the expected text.
    
    Args:
        expected_text (str): The expected text to compare with.

    Returns:
        Callable: A function that checks if the event text or caption or callbackQuery data is equal to the expected text.
    """
    async def check(event, *args):
        try:
            if isinstance(expected_text, str):
                return getattr(event, "text", None) == expected_text or getattr(event, "caption", None) == expected_text or getattr(event, "data", None) == expected_text
            else:
                return getattr(event, "text", None) in expected_text or getattr(event, "caption", None) in expected_text or getattr(event, "data", None) in expected_text
        except:
            return False
    return Filter(check)

def startswith(expected_text: Union[str, List[str]]):
    """
    Check if the event text or caption or callbackQuery data is started with to the expected text.
    
    Args:
        expected_text (str): The expected text to compare with.

    Returns:
        Callable: A function that checks if the event text or caption or callbackQuery data is started with to the expected text.
    """
    async def check(event, *args):
        try:
            if isinstance(expected_text, str):
                return getattr(event, "text", "").startswith(expected_text) or getattr(event, "caption", "").startswith(expected_text) or getattr(event, "data", "").startswith(expected_text)
            else:
                e_texts = [getattr(event, "text", "").startswith(expected_textt) or getattr(event, "caption", "").startswith(expected_textt) or getattr(event, "data", "").startswith(expected_textt) for expected_textt in expected_text]
                for e in e_texts:
                    if e:
                        return True

            return False
        except:
            return False
    return Filter(check)


def regex(pattern: str):
    """
    checks the event text or caption with given pattern using regex
    
    Args:
        pattern (str): The pattern to check with text
    
    Returns:
        Callable: A function that checks if the event text or caption is match with given pattern
    """
    async def check(event, *args):
        try:
            return re.search(pattern, getattr(event, "text", "")) or re.search(pattern, getattr(event, "caption", ""))
        except:
            return False
    return Filter(check)

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
    async def check(event, *args):
        try:
            event_user = getattr(event, "user", None)
            event_user_id = getattr(event_user, "id")
            if event_user_id in allowed_users:
                return True
        except:
            return False
    return Filter(check)

def is_joined(chat_ids: Union[List[Union["User", int, str]], int, str]):
    """
    Checks if the event User is joined in specified chats.
    
    Args:
        allowed_users (List[Union["User", int]]): Allowed users to use this handler.

    Returns:
        Callable: A function that checks if the event User is joined in specified chats
    """
    if type(chat_ids) in [str, int]:
        try:
            chat_ids = [int(chat_ids)]
        except:
            raise ValueError("Chat IDs can only be digits")

    async def check(event, client: 'Client', *args):
        try:
            event_user = getattr(event, "user", None)
            event_user_id = getattr(event_user, "id")
            for chat in chat_ids:
                data = await client.make_post(
                    client.requests_base + "/getChatMember",
                    data={"chat_id": chat, "user_id": event_user_id},
                )
                joined = data.get("result", {}).get("status") in ["member", "creator", "administrator"]
                if not joined:
                    return False
            return True
            
        except:
            return False
    return Filter(check)

def at_state(state: Optional[str] = None):
    """
    Checks if the event User is at specified state.
    
    Args:
        state (Optional[str]): state condition

    Returns:
        Callable: A function that checks if the event User is at specified state.
    
    """

    async def check(event, client: 'Client', *args):
        try:
            event_user = getattr(event, "user", None)
            event_user_id = getattr(event_user, "id")
            return client.state_machine.get_state(event_user_id) == state
        except:
            return False
    return Filter(check)

def _private():
    """
    checks if the event is happening in a private chat
    """

    async def check(event, *args):
        try:
            chat = getattr(event, "chat")
            return getattr(chat, "private")
        except:
            return False
    return Filter(check)

def _group():
    """
    checks if the event is happening in a group chat
    """

    async def check(event, *args):
        try:
            chat = getattr(event, "chat")
            return chat.type == chat.type.GROUP
        except:
            return False
    return Filter(check)

def _reply():
    """
    Checks if the event is a reply to a message.
    """

    async def check(event, *args):
        try:
            return getattr(event, "reply_to_message") is not None
        except:
            return False
    return Filter(check)

def _forward():
    """
    Checks if the event is a forwarded message.
    """

    async def check(event, *args):
        try:
            return getattr(event, "forward_from") is not None
        except:
            return False
    return Filter(check)

def _gif():
    """
    Checks if the event has a gif media.
    """

    async def check(event, *args):
        try:
            return getattr(event, "animation") is not None
        except:
            return False
    return Filter(check)

def _digit():
    """
    Check if the event text or caption or callbackQuery data is digit.
    
    Returns:
        Callable: A function that checks if the event text or caption or callbackQuery data is digit.
    """
    async def check(event, *args):
        try:
            return getattr(event, "text", "").isdigit() or getattr(event, "caption", "").isdigit() or getattr(event, "data", "").isdigit()
        except:
            return False
    return Filter(check)

def _channel():
    """
    checks if the event is happening in a channel
    """

    async def check(event, args):
        try:
            chat = getattr(event, "chat")
            return getattr(chat, "channel")
        except:
            return False
    return Filter(check)

def func(function: Callable):
    async def check(event, *args):
        try:
            return function(event)
        except:
            return False
    return Filter(check)


def _text():
    async def check(event, *args):
        return hasattr(event, "text") and bool(getattr(event, "text"))
    return Filter(check)

def _photo():
    async def check(event, *args):
        return hasattr(event, "photo") and bool(getattr(event, "photo"))
    return Filter(check)

def _video():
    async def check(event, *args):
        return hasattr(event, "video") and bool(getattr(event, "video"))
    return Filter(check)

def _audio():
    async def check(event, *args):
        return hasattr(event, "audio") and bool(getattr(event, "audio"))
    return Filter(check)

def _voice():
    async def check(event, *args):
        return hasattr(event, "voice") and bool(getattr(event, "voice"))
    return Filter(check)

def _contact():
    async def check(event, *args):
        return hasattr(event, "contact") and bool(getattr(event, "contact"))
    return Filter(check)

def _location():
    async def check(event, *args):
        return hasattr(event, "location") and bool(getattr(event, "location"))
    return Filter(check)

private = pv = _private()
channel = _channel()
group = _group()
digit = _digit()
reply = _reply()
forward = _forward()
gif = _gif()
text = _text()
photo = _photo()
video = _video()
audio = _audio()
voice = _voice()
contact = _contact()
location = _location()