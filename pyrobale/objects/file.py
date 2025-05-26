class File:
    """A class representing a file object."""

    def __init__(
        self,
        file_id: str,
        file_unique_id: str,
        file_size: int,
        file_path: str,
        **kwargs
    ):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_size = file_size
        self.file_path = file_path
