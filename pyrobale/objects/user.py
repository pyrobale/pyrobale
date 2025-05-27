from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
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
        self.client: Optional["Client"] = kwargs.get("client", None)
