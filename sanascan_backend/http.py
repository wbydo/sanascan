import json

import falcon


class HelloWorldResource:
    def on_get(self, req, resp):
        resp.data = json.dumps(
            {'hello': 'world'}
        ).encode('utf-8')
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200


api = falcon.API()
hello = HelloWorldResource()
api.add_route('/', hello)
