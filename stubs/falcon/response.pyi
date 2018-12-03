from typing import Optional

class Response:
    data: Optional[bytes]
    content_type: Optional[str]
    status: Optional[str]

    def append_header(self, name: str, value: str) -> None: ...
