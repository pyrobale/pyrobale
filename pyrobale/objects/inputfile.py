import aiohttp
import asyncio
import os
from typing import Dict, Union, Optional
from io import BufferedReader, BytesIO
import mimetypes

class InputFile:
    def __init__(self, file_input: Union[str, "BufferedReader", bytes], *, file_name: Optional[str] = None) -> None:
        if not isinstance(file_input, (str, BufferedReader, bytes)):
            raise TypeError(
                "file_input parameter must be one of str, BufferedReader, and byte types"
            )

        self._file_handle = None
        self._should_close = False

        if isinstance(file_input, str):
            if not os.path.exists(file_input):
                raise FileNotFoundError(f"File not found: {file_input}")
            
            self._file_handle = open(file_input, "rb")
            self._should_close = True
            file_content = self._file_handle.read()
            if not file_name:
                file_name = os.path.basename(file_input)
                
        elif isinstance(file_input, BufferedReader):
            current_pos = file_input.tell()
            file_content = file_input.read()
            file_input.seek(current_pos) 
            
            if not file_name and hasattr(file_input, 'name'):
                file_name = os.path.basename(file_input.name)
        else:
            file_content = file_input

        if file_name and not isinstance(file_name, str):
            raise TypeError("file_name param must be type of str")

        self.file_input: bytes = file_content
        self.file_name: Optional[str] = file_name

    def __del__(self):
        """Ensure file handle is closed when object is destroyed"""
        if self._should_close and self._file_handle and not self._file_handle.closed:
            self._file_handle.close()

    def close(self):
        """Explicitly close the file handle if needed"""
        if self._should_close and self._file_handle and not self._file_handle.closed:
            self._file_handle.close()

    def to_multipart_payload(self) -> Dict:
        payload = {
            "value": self.file_input,
            "content_type": "multipart/form-data"
        }
        if self.file_name:
            payload["filename"] = self.file_name

        return payload