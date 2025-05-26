from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .utils import build_api_url
    from .photosize import PhotoSize


class Animation:
    """Represents an animation file (GIF or H.264/MPEG-4 AVC video without
    sound) to be sent."""

    def __init__(
        self,
        file_id: Optional[str] = None,
        file_unique_id: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        duration: Optional[int] = None,
        thumb: Optional["PhotoSize"] = None,
        file_name: Optional[str] = None,
        mime_type: Optional[str] = None,
        file_size: Optional[int] = None,
        **kwargs
    ):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.duration = duration
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
