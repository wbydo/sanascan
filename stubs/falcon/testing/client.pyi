from typing import Any, Dict


class TestClient:
    def simulate_get(self, path: str = ...,  **kwargs: Any) -> Result: ...
    def simulate_post(self, path: str = ..., **kwargs: Any) -> Result: ...
    def simulate_put(self, path: str = ..., *, params: Dict[str, str], **kwargs: Any) -> Result: ...

class Result:
    status_code: int
    json: Any
