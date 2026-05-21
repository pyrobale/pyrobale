from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .utils import build_api_url
    from .photosize import PhotoSize


class Document:
    """Represents a general file to be sent without any special properties."""

    def __init__(
        self,
        file_id: str,
        file_unique_id: str,
        thumbnail: Optional["PhotoSize"] = None,
        file_name: Optional[str] = None,
        mime_type: Optional[str] = None,
        file_size: Optional[int] = None,
        **kwargs
    ):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.thumbnail = thumbnail
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
