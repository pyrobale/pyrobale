import re
from typing import Callable, List, Optional, Union, TYPE_CHECKING
import inspect

if TYPE_CHECKING:
    from ..objects.user import User
    from ..client import Client


class Filter:
    __slots__ = ('check_func', '_num_params')

    def __init__(self, check_func: Callable, num_params: int = None):
        self.check_func = check_func
        if num_params is None:
            sig = inspect.signature(check_func)
            self._num_params = len(sig.parameters)
        else:
            self._num_params = num_params

    def __call__(self, event, client=None, *args, **kwargs) -> bool:
        try:
            if self._num_params >= 2:
                return self.check_func(event, client, *args, **kwargs)
            else:
                return self.check_func(event, *args, **kwargs)
        except Exception:
            return False

    def __and__(self, other: 'Filter') -> 'Filter':
        return CombinedFilter(self, other, 'and')

    def __or__(self, other: 'Filter') -> 'Filter':
        return CombinedFilter(self, other, 'or')

    def __invert__(self) -> 'Filter':
        return NegatedFilter(self)


class NegatedFilter(Filter):
    __slots__ = ('original',)

    def __init__(self, original: Filter):
        self.original = original

    def __call__(self, event, client=None, *args, **kwargs) -> bool:
        return not self.original(event, client, *args, **kwargs)


class CombinedFilter(Filter):
    __slots__ = ('left', 'right', 'operator')

    def __init__(self, left: Filter, right: Filter, operator: str):
        self.left = left
        self.right = right
        self.operator = operator

    def __call__(self, event, client=None, *args, **kwargs) -> bool:
        left_result = self.left(event, client, *args, **kwargs)
        if self.operator == 'and':
            return left_result and self.right(event, client, *args, **kwargs)
        elif self.operator == 'or':
            return left_result or self.right(event, client, *args, **kwargs)
        raise ValueError(f"Invalid operator: {self.operator}")


def equals(expected_text: str) -> Filter:
    def check(event, *args):
        try:
            return (getattr(event, "text", None) == expected_text or
                    getattr(event, "caption", None) == expected_text or
                    getattr(event, "data", None) == expected_text)
        except:
            return False
    return Filter(check, num_params=1)


def startswith(expected_text: str) -> Filter:
    def check(event, *args):
        try:
            return (getattr(event, "text", "").startswith(expected_text) or
                    getattr(event, "caption", "").startswith(expected_text) or
                    getattr(event, "data", "").startswith(expected_text))
        except:
            return False
    return Filter(check, num_params=1)


def regex(pattern: str) -> Filter:
    def check(event, *args):
        try:
            return (re.search(pattern, getattr(event, "text", "")) or
                    re.search(pattern, getattr(event, "caption", "")))
        except:
            return False
    return Filter(check, num_params=1)


def from_users(allowed_users: Union[List[Union["User", int, str]], int, str]) -> Filter:
    if isinstance(allowed_users, (str, int)):
        try:
            allowed_users = [int(allowed_users)]
        except:
            raise ValueError("Chat IDs can only be digits")

    def check(event, client=None):
        try:
            event_user = getattr(event, "user", None)
            event_user_id = getattr(event_user, "id")
            return event_user_id in allowed_users
        except:
            return False
    return Filter(check, num_params=2)


def is_joined(chat_ids: Union[List[Union["User", int, str]], int, str]) -> Filter:
    if isinstance(chat_ids, (str, int)):
        try:
            chat_ids = [int(chat_ids)]
        except:
            raise ValueError("Chat IDs can only be digits")

    def check(event, client: 'Client'):
        try:
            event_user = getattr(event, "user", None)
            event_user_id = getattr(event_user, "id")
            for chat in chat_ids:
                if not client.is_joined(event_user_id, chat):
                    return False
            return True
        except:
            return False
    return Filter(check, num_params=2)


def at_state(state: Optional[str] = None) -> Filter:
    def check(event, client: 'Client'):
        try:
            event_user = getattr(event, "user", None)
            event_user_id = getattr(event_user, "id")
            return client.state_machine.get_state(event_user_id) == state
        except:
            return False
    return Filter(check, num_params=2)


def func(function: Callable) -> Filter:
    sig = inspect.signature(function)
    num_params = len(sig.parameters)
    return Filter(function, num_params=num_params)


def _private_check(event, client=None):
    try:
        chat = getattr(event, "chat")
        return getattr(chat, "private", False)
    except:
        return False
private = pv = Filter(_private_check, num_params=2)


def _group_check(event, client=None):
    try:
        chat = getattr(event, "chat")
        return chat.type == "group"
    except:
        return False
group = Filter(_group_check, num_params=2)


def _channel_check(event, client=None):
    try:
        chat = getattr(event, "chat")
        return chat.type == "channel"
    except:
        return False
channel = Filter(_channel_check, num_params=2)


def _digit_check(event, client=None):
    try:
        return (getattr(event, "text", "").isdigit() or
                getattr(event, "caption", "").isdigit() or
                getattr(event, "data", "").isdigit())
    except:
        return False
digit = Filter(_digit_check, num_params=2)


def _reply_check(event, client=None):
    try:
        return getattr(event, "reply_to_message") is not None
    except:
        return False
reply = Filter(_reply_check, num_params=2)


def _forward_check(event, client=None):
    try:
        return getattr(event, "forward_origin") is not None
    except:
        return False
forward = Filter(_forward_check, num_params=2)


def _gif_check(event, client=None):
    try:
        return getattr(event, "animation") is not None
    except:
        return False
gif = Filter(_gif_check, num_params=2)


text = TEXT = "text"
photo = PHOTO = "photo"
video = VIDEO = "video"
audio = AUDIO = "audio"
voice = VOICE = "voice"
contact = CONTACT = "contact"
location = LOCATION = "location"


__all__ = [
    "Filter", "NegatedFilter", "CombinedFilter",
    "equals", "startswith", "regex", "from_users", "is_joined", "at_state", "func",
    "private", "pv", "group", "channel", "digit", "reply", "forward", "gif",
    "text", "TEXT", "photo", "PHOTO", "video", "VIDEO",
    "audio", "AUDIO", "voice", "VOICE", "contact", "CONTACT", "location", "LOCATION"
]