from typing import List, Union


class InputFile:
    def __init__(self, file: Union[bytes, str], **kwargs):
        """
        Initialize an InputFile object that can handle file uploads in 3 ways:
        1. Using file_id for files already on Bale servers
        2. Using HTTP URL for remote files (5MB limit for images, 20MB for other content)
        3. Using multipart/form-data upload (10MB limit for images, 50MB for other content)

        Args:
            file: Can be either:
                - bytes: For direct file upload
                - str: For file_id or HTTP URL
        """
        self.file = file
