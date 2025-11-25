from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from pyrobale import Chat


class ForwardOrigin:
    def __init__(self,
                 type: Union[str, None] = None,
                 date: Union[str, int, None] = None,
                 message_id: Union[int, None] = None,
                 chat: Union["Chat", dict, None] = None,
                 **kwargs):
        self.type = type
        self.date = date
        self.client = kwargs.get("client")
        if isinstance(chat, dict):
            from pyrobale import Chat
            self.chat = Chat(**chat, client=self.client)
        else:
            self.chat = chat
        self.message_id = message_id