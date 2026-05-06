from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import Client
    from ..objects import User


class User:
    def __init__(
        self,
        id: Optional[int],
        is_bot: bool,
        first_name: str,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
        language_code: Optional[str] = None,
        **kwargs
    ):
        self.id = int(id)
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.client: Client = kwargs.get("client")
        self.language_code = language_code
    
    def set_state(self, state: str):
        self.client.state_machine.set_state(self.id, state)
    
    def del_state(self):
        self.client.state_machine.del_state(self.id)
    
    def get_state(self):
        self.client.state_machine.get_state(self.id)