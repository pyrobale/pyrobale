import re
from typing import Callable, List, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ..objects.user import User
    from ..client import Client

class Filter:
    def __init__(self, check_func: Callable) -> None:
        self.check = check_func
        self.lst = [check_func]
        self.inv = False
    
    def __invert__(self):
        new_filter = Filter(self.check)
        new_filter.inv = True
        new_filter.lst = self.lst.copy()
        return new_filter
    
    def __and__(self, other):
        if not isinstance(other, Filter):
            raise TypeError(f"Cannot combine Filter with {type(other)}")
        
        def combined_check(event, client=None, *args):
            if self.inv:
                result1 = not self.check(event, client, *args)
            else:
                result1 = self.check(event, client, *args)
            
            if other.inv:
                result2 = not other.check(event, client, *args)
            else:
                result2 = other.check(event, client, *args)
            
            return result1 and result2
        
        new = Filter(combined_check)
        new.lst = self.lst + other.lst
        return new
    
    def __call__(self, event, client=None, *args):
        if self.inv:
            return not self.check(event, client, *args)
        return self.check(event, client, *args)


class equals(Filter):
    def __init__(self, expected_text: str):
        def check(event, *args):
            try:
                return (getattr(event, "text", None) == expected_text or 
                       getattr(event, "caption", None) == expected_text or 
                       getattr(event, "data", None) == expected_text)
            except:
                return False
        super().__init__(check)


class startswith(Filter):
    def __init__(self, expected_text: str):
        def check(event, *args):
            try:
                return (getattr(event, "text", "").startswith(expected_text) or 
                       getattr(event, "caption", "").startswith(expected_text) or 
                       getattr(event, "data", "").startswith(expected_text))
            except:
                return False
        super().__init__(check)


class regex(Filter):
    def __init__(self, pattern: str):
        def check(event, *args):
            try:
                return (re.search(pattern, getattr(event, "text", "")) or 
                       re.search(pattern, getattr(event, "caption", "")))
            except:
                return False
        super().__init__(check)


class from_users(Filter):
    def __init__(self, allowed_users: Union[List[Union["User", int, str]], int, str]):
        if type(allowed_users) in [str, int]:
            try:
                allowed_users = [int(allowed_users)]
            except:
                raise ValueError("Chat IDs can only be digits")
        
        def check(event, *args):
            try:
                event_user = getattr(event, "user", None)
                event_user_id = getattr(event_user, "id") if event_user else None
                return event_user_id in allowed_users if event_user_id else False
            except:
                return False
        super().__init__(check)


class is_joined(Filter):
    def __init__(self, chat_ids: Union[List[Union["User", int, str]], int, str]):
        if type(chat_ids) in [str, int]:
            try:
                chat_ids = [int(chat_ids)]
            except:
                raise ValueError("Chat IDs can only be digits")
        
        def check(event, client: 'Client', *args):
            try:
                event_user = getattr(event, "user", None)
                event_user_id = getattr(event_user, "id") if event_user else None
                if not event_user_id:
                    return False
                
                for chat in chat_ids:
                    joined = client.is_joined(event_user_id, chat)
                    if not joined:
                        return False
                return True
            except:
                return False
        super().__init__(check)


class at_state(Filter):
    def __init__(self, state: Optional[str] = None):
        def check(event, client: 'Client', *args):
            try:
                event_user = getattr(event, "user", None)
                event_user_id = getattr(event_user, "id") if event_user else None
                if not event_user_id:
                    return False
                return client.state_machine.get_state(event_user_id) == state
            except:
                return False
        super().__init__(check)


class private(Filter):
    def __init__(self):
        def check(event, *args):
            try:
                chat = getattr(event, "chat")
                return getattr(chat, "private", False)
            except:
                return False
        super().__init__(check)


class group(Filter):
    def __init__(self):
        def check(event, *args):
            try:
                chat = getattr(event, "chat")
                return chat.type == chat.type.GROUP if hasattr(chat, 'type') else False
            except:
                return False
        super().__init__(check)


class reply(Filter):
    def __init__(self):
        def check(event, *args):
            try:
                return getattr(event, "reply_to_message") is not None
            except:
                return False
        super().__init__(check)


class forward(Filter):
    def __init__(self):
        def check(event, *args):
            try:
                return getattr(event, "forward_from") is not None
            except:
                return False
        super().__init__(check)


class gif(Filter):
    def __init__(self):
        def check(event, *args):
            try:
                return getattr(event, "animation") is not None
            except:
                return False
        super().__init__(check)


class digit(Filter):
    def __init__(self):
        def check(event, *args):
            try:
                return (getattr(event, "text", "").isdigit() or 
                       getattr(event, "caption", "").isdigit() or 
                       getattr(event, "data", "").isdigit())
            except:
                return False
        super().__init__(check)


class channel(Filter):
    def __init__(self):
        def check(event, args):
            try:
                chat = getattr(event, "chat")
                return getattr(chat, "channel", False)
            except:
                return False
        super().__init__(check)


class func(Filter):
    def __init__(self, function: Callable):
        def check(event, *args):
            try:
                return function(event)
            except:
                return False
        super().__init__(check)


class text(Filter):
    def __init__(self):
        def check(event, *args):
            try:
                return getattr(event, "text") is not None
            except:
                return False
        super().__init__(check)

class photo(Filter):
    def __init__(self):
        def check(event, *args):
            try:
                return getattr(event, "photo") is not None
            except:
                return False
        super().__init__(check)

class video(Filter):
    def __init__(self):
        def check(event, *args):
            try:
                return getattr(event, "video") is not None
            except:
                return False
        super().__init__(check)

class audio(Filter):
    def __init__(self):
        def check(event, *args):
            try:
                return getattr(event, "audio") is not None
            except:
                return False
        super().__init__(check)

class voice(Filter):
    def __init__(self):
        def check(event, *args):
            try:
                return getattr(event, "voice") is not None
            except:
                return False
        super().__init__(check)

class contact(Filter):
    def __init__(self):
        def check(event, *args):
            try:
                return getattr(event, "contact") is not None
            except:
                return False
        super().__init__(check)

class location(Filter):
    def __init__(self):
        def check(event, *args):
            try:
                return getattr(event, "location") is not None
            except:
                return False
        super().__init__(check)

pv= private = private()  # type: ignore
group = group()# type: ignore
reply = reply()# type: ignore
forward = forward()# type: ignore
gif = gif()# type: ignore
digit = digit()# type: ignore
channel = channel()# type: ignore
text = text()# type: ignore
photo = photo()# type: ignore
video = video()# type: ignore
audio = audio()# type: ignore
voice = voice()# type: ignore
contact = contact()# type: ignore
location = location()# type: ignore
TEXT = text
PHOTO = photo
VIDEO = video
AUDIO = audio
VOICE = voice
CONTACT = contact
LOCATION = location

