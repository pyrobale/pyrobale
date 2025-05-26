class InputMedia:
    """Base class for all input media types.

    This is an abstract class that should not be used directly.
    """

    def __init__(self, media, caption=None):
        """Initialize the base InputMedia object.

        Args:
            media (str): File to send. Can be a file_id, HTTP URL, or "<attach://file_attach_name>".
            caption (str, optional): Caption for the media, 0-1024 characters.
        """
        self.media = media
        self.caption = caption


class InputMediaPhoto(InputMedia):
    """Represents a photo to be sent.

    This object represents a photo that needs to be sent to Bale.
    """

    def __init__(self, media, caption=None):
        """Initialize an InputMediaPhoto object.

        Args:
            media (str): File to send. Can be:
                1) A file_id to send a file that exists on Bale servers (recommended)
                2) An HTTP URL for Bale to get a file from the Internet
                3) "<attach://file_attach_name>" to upload a new file using multipart/form-data
            caption (str, optional): Caption for the photo, 0-1024 characters.
        """
        super().__init__(media, caption)
        self.type = "photo"


class InputMediaVideo(InputMedia):
    """Represents a video to be sent.

    This object represents a video that needs to be sent to Bale.
    """

    def __init__(
        self,
        media,
        caption=None,
        thumbnail=None,
        width=None,
        height=None,
        duration=None,
    ):
        """Initialize an InputMediaVideo object.

        Args:
            media (str): File to send. Can be:
                1) A file_id to send a file that exists on Bale servers (recommended)
                2) An HTTP URL for Bale to get a file from the Internet
                3) "<attach://file_attach_name>" to upload a new file using multipart/form-data
            caption (str, optional): Caption for the video, 0-1024 characters.
            thumbnail (InputFile or str, optional): Thumbnail of the video.
                Should be in JPEG format and less than 200 KB in size.
                Width and height should not exceed 320px.
            width (int, optional): Video width.
            height (int, optional): Video height.
            duration (int, optional): Video duration in seconds.
        """
        super().__init__(media, caption)
        self.type = "video"
        self.thumbnail = thumbnail
        self.width = width
        self.height = height
        self.duration = duration


class InputMediaAnimation(InputMedia):
    """Represents an animation to be sent.

    This object represents an animation file (GIF or H.264/MPEG-4 AVC
    video without sound) that needs to be sent to Bale.
    """

    def __init__(
        self,
        media,
        caption=None,
        thumbnail=None,
        width=None,
        height=None,
        duration=None,
    ):
        """Initialize an InputMediaAnimation object.

        Args:
            media (str): File to send. Can be:
                1) A file_id to send a file that exists on Bale servers (recommended)
                2) An HTTP URL for Bale to get a file from the Internet
                3) "<attach://file_attach_name>" to upload a new file using multipart/form-data
            caption (str, optional): Caption for the animation, 0-1024 characters.
            thumbnail (InputFile or str, optional): Thumbnail of the animation.
                Should be in JPEG format and less than 200 KB in size.
                Width and height should not exceed 320px.
            width (int, optional): Animation width.
            height (int, optional): Animation height.
            duration (int, optional): Animation duration in seconds.
        """
        super().__init__(media, caption)
        self.type = "animation"
        self.thumbnail = thumbnail
        self.width = width
        self.height = height
        self.duration = duration


class InputMediaAudio(InputMedia):
    """Represents an audio file to be sent.

    This object represents an audio file that needs to be sent to Bale.
    The file will be treated as music.
    """

    def __init__(self, media, caption=None, thumbnail=None, duration=None, title=None):
        """Initialize an InputMediaAudio object.

        Args:
            media (str): File to send. Can be:
                1) A file_id to send a file that exists on Bale servers (recommended)
                2) An HTTP URL for Bale to get a file from the Internet
                3) "<attach://file_attach_name>" to upload a new file using multipart/form-data
            caption (str, optional): Caption for the audio file, 0-1024 characters.
            thumbnail (InputFile or str, optional): Thumbnail of the audio file.
                Should be in JPEG format and less than 200 KB in size.
                Width and height should not exceed 320px.
            duration (int, optional): Duration of the audio in seconds.
            title (str, optional): Title of the audio.
        """
        super().__init__(media, caption)
        self.type = "audio"
        self.thumbnail = thumbnail
        self.duration = duration
        self.title = title


class InputMediaDocument(InputMedia):
    """Represents a document to be sent.

    This object represents a general file (document) that needs to be
    sent to Bale.
    """

    def __init__(self, media, caption=None, thumbnail=None):
        """Initialize an InputMediaDocument object.

        Args:
            media (str): File to send. Can be:
                1) A file_id to send a file that exists on Bale servers (recommended)
                2) An HTTP URL for Bale to get a file from the Internet
                3) "<attach://file_attach_name>" to upload a new file using multipart/form-data
            caption (str, optional): Caption for the document, 0-1024 characters.
            thumbnail (InputFile or str, optional): Thumbnail of the document.
                Should be in JPEG format and less than 200 KB in size.
                Width and height should not exceed 320px.
        """
        super().__init__(media, caption)
        self.type = "document"
        self.thumbnail = thumbnail
