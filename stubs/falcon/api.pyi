from typing import Any, Union
from typing_extensions import Protocol

from .request import Request as Request
from .response import Response as Response


class OnGetResource(Protocol):
    def on_get(self, req: Request, resp: Response) -> None: ...

class OnPostResource(Protocol):
    def on_post(self, req: Request, resp: Response) -> None: ...

Resource = Union[OnGetResource, OnPostResource]

class API(object):
    def add_route(self, uri_template: str, resource: Resource, *args: Any, **kwargs: Any) -> None: ...
