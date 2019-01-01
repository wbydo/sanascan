from typing import Optional, Any, Iterable
from .node import MeCabNode


class MeCab:
    def __init__(self, options: Optional[Any] = ..., **kwargs: Any) -> None: ...
    def parse(self, text: str, **kwargs: Any) -> Iterable[MeCabNode]: ...
