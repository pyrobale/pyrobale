class Audio:
    """
    Represents an audio file to be treated as music to be sent.
    """
    def __init__(self, file_id: str, file_unique_id: str, duration: int, title: str, file_name: str, mime_type: str, file_size: int):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.title = title
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size