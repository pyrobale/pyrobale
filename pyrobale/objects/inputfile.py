from typing import Dict, Union, Optional
from io import BufferedReader, BytesIO


class InputFile:
    def __init__(self, file_input: str | "BufferedReader" | bytes, *, file_name: Optional[str] = None) -> None:
        if not isinstance(file_input, (str, BufferedReader, bytes)):
            raise TypeError(
                "file_input parameter must be one of str, BufferedReader, and byte types"
            )

        if isinstance(file_input, str):
            file_input = file_input.encode()
        elif isinstance(file_input, BufferedReader):
            file_input = file_input.read()

        if file_name:
            if not isinstance(file_name, str):
                raise TypeError(
                    "file_name param must be type of str"
                )

        self.file_input: Union[bytes, str] = file_input
        self.file_name: Optional[str] = file_name

    def to_multipart_payload(self) -> Dict:
        payload = {
            "value": self.file_input,
            "content_type": "multipart/form-data"
        }
        if self.file_name:
            payload["filename"] = self.file_name

        return payload
