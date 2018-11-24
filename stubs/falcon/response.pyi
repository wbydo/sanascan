from typing import Optional

class Response:
    data: Optional[bytes]
    content_type: Optional[str]
    status: Optional[str]
