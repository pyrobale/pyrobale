from typing import Any
from .user import User


class InviteLink:
    def __init__(self, invite_link: str, creator: dict, creates_join_request: bool, is_primary: bool,
                 is_revoked: bool, name: str, expire_date: int, member_limit: int, pending_join_request_count: int):
        self.invite_link = invite_link
        self.creator = User(**creator)
        self.creates_join_request = creates_join_request
        self.is_primary = is_primary
        self.is_revoked = is_revoked
        self.member_limit = member_limit
        self.pending_join_request_count = pending_join_request_count
        self.expire_date = expire_date
        self.name = name

    def to_url(self):
        return f"https://{self.invite_link}"

    @property
    def url(self):
        return f"https://{self.invite_link}"
