from typing import Any


class TestClient:
    def simulate_get(self, path: str = ..., **kwargs: Any) -> Result: ...


class Result:
    json: Any
