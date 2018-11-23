from typing import Any
from typing_extensions import Protocol

from .request import Request as Request
from .response import Response as Response


class OnGetResource(Protocol):
    def on_get(self, req: Request, resp: Response) -> None: ...

class API(object):
    def add_route(self, uri_template: str, resource: OnGetResource, *args: Any, **kwargs: Any) -> None: ...
