from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .sticker import Sticker
    from .photosize import PhotoSize


class StickerSet:
    def __init__(
        self, name: str, title: str, stickers: List["Sticker"], thumb: "PhotoSize"
    ):
        pass
