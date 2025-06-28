class PeerData:
    """A class to parse data received from ble.ir pages."""
    def __init__(self,
                 is_ok: bool,
                 avatar: str,
                 description: str,
                 name: str,
                 is_bot: bool,
                 is_verified: bool,
                 is_private: bool,
                 members: int,
                 last_message: str,
                 user_id: int,
                 username: str):
        self.is_ok = is_ok
        self.avatar = avatar
        self.description = description
        self.name = name
        self.is_bot = is_bot
        self.is_verified = is_verified
        self.is_private = is_private
        self.members = members
        self.last_message = last_message
        self.user_id = user_id
        self.username = username