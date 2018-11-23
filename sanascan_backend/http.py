import json

from falcon import API, MEDIA_JSON, HTTP_200, Request, Response


class HelloWorldResource:
    def on_get(self, req: Request, resp: Response) -> None:
        resp.data = json.dumps(
            {'hello': 'world'}
        ).encode('utf-8')
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200


api = API()
hello = HelloWorldResource()
api.add_route('/', hello)
