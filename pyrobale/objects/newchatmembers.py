from .user import User
from .chat import Chat
from typing import List

class NewChatMembers:
    def __init__(self, inviter: User, date: int, chat: Chat, new_chat_members: List["User"]) -> None:
        self.inviter = inviter
        self.date = date
        self.chat = chat
        self.new_chat_members = new_chat_members