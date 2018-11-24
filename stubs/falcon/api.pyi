from typing import Any, Union
from typing_extensions import Protocol

from .request import Request as Request
from .response import Response as Response


class OnGetResource(Protocol):
    def on_get(self, req: Request, resp: Response, *, eid: int) -> None: ...

class OnPostResource(Protocol):
    def on_post(self, req: Request, resp: Response, *, eid: int) -> None: ...

class OnPutResource(Protocol):
    def on_put(self, req: Request, resp: Response, *, eid: int) -> None: ...

Resource = Union[
    OnGetResource,
    OnPostResource,
    OnPutResource
]

class API(object):
    def add_route(self, uri_template: str, resource: Resource, *args: Any, **kwargs: Any) -> None: ...
