from typing import Optional
from ..client import Client


class User:
    def __init__(
        self,
        id: int = None,
        is_bot: bool = None,
        first_name: str = None,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
        **kwargs
    ):
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.client: Client = kwargs.get("kwargs", {}).get("client")
    
    def set_state(self, state: str):
        self.client.state_machine.set_state(self.id, state)
    
    def del_state(self, state: str):
        self.client.state_machine.del_state(self.id)
