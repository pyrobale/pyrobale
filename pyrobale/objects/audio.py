from typing import Optional


class Audio:
    """Represents an audio file to be treated as music to be sent."""

    def __init__(
        self,
        file_id: Optional[str] = None,
        file_unique_id: Optional[str] = None,
        duration: Optional[int] = None,
        title: Optional[str] = None,
        file_name: Optional[str] = None,
        mime_type: Optional[str] = None,
        file_size: Optional[int] = None,
        **kwargs
    ):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.title = title
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
