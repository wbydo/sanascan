from typing import Any


class TestClient:
    def simulate_get(self, path: str = ..., **kwargs: Any) -> Result: ...
    def simulate_post(self, path: str = ..., **kwargs: Any) -> Result: ...


class Result:
    json: Any
