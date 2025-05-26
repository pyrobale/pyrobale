from typing import Optional


class ChatPhoto:
    """This object represents a chat photo."""

    def __init__(
        self,
        small_file_id: Optional[str] = None,
        small_file_unique_id: Optional[str] = None,
        big_file_id: Optional[str] = None,
        big_file_unique_id: Optional[str] = None,
        **kwargs
    ):
        self.small_file_id = small_file_id
        self.small_file_unique_id = small_file_unique_id
        self.big_file_id = big_file_id
        self.big_file_unique_id = big_file_unique_id
