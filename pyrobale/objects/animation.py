from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .utils import build_api_url
    from .photosize import PhotoSize

class Animation:
    """
    Represents an animation file (GIF or H.264/MPEG-4 AVC video without sound) to be sent.
    """
    def __init__(self, file_id: str, file_unique_id: str, width: int, height: int, duration: int, thumb: 'PhotoSize', file_name: str, mime_type: str, file_size: int):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.duration = duration
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size