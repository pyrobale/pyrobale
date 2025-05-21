from typing import Optional, Union
from .utils import build_api_url
import asyncio
import aiohttp

class User:
    def __init__(self, id: int, is_bot: bool, first_name: str, last_name: Optional[str], username: Optional[str]):
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        self.username = username