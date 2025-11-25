from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..objects.chat import Chat
    from ..objects.user import User

typee = type

class ForwardOrigin:
    def __init__(self,
                 type: Union[str, None] = None,
                 date: Union[str, int, None] = None,
                 message_id: Union[int, None] = None,
                 chat: Union["Chat", dict, None] = None,
                 sender_user: Union["User", dict, None] = None,
                 **kwargs):
        self.type = type
        self.date = date
        self.client = kwargs.get("client")
        from ..objects.chat import Chat
        from ..objects.user import User

        if isinstance(chat, dict):
            self.chat = Chat(**chat, client=self.client)
        elif isinstance(chat, Chat):
            self.chat = chat

        if isinstance(sender_user, dict):
            self.sender_user = User(**sender_user, client=self.client)
        else:
            self.sender_user = sender_user

        if sender_user:
            self.forwarded_from = self.sender_user

        if chat:
            self.forwarded_from = self.chat

        self.message_id = message_id