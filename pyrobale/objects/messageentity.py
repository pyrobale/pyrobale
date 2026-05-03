from typing import Union
from .enums import MessageEntityType



class MessageEntity:
    """An object that represents a certain part of message text, like mentions or commands

    Parameters:
        type (str or MessageEntityType): The certain part of message type.
        offset (int): Location of that part in message text.
        length (int): the length of that part in message text.

    Attributes:
        type (MessageEntityType): The certain part of message type.
        offset (int): Location of that part in message text.
        length (int): the length of that part in message text.
    """

    def __init__(self,
        type: Union[str, MessageEntityType],
        offset: int,
        length: int
    ):
        if isinstance(type, str):
            self.type = MessageEntityType(type)
        else:
            self.type = type
        
        self.offset = offset
        self.length = length