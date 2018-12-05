from typing import Dict
from pathlib import Path
import json

from falcon import API, MEDIA_JSON, Request, Response
from falcon import HTTP_200, HTTP_201

from .estimator import Estimator
from .lang_model import LangModel
from .word import Word, TagWord
from .key import Key


class CORSMiddleware:
    def process_request(self, req: Request, resp: Response) -> None:
        resp.set_header('Access-Control-Allow-Origin', '*')


class RootResource:
    _estimators: Dict[int, Estimator]
    _lm: LangModel

    def __init__(self) -> None:
        self._estimators = {}

        # あとで変更
        with (Path.home() / 'arpa/LM0006.txt').open() as f:
            self._lm = LangModel(f.read())

    def on_post(self, req: Request, resp: Response, *, eid: int = 0) -> None:
        if not eid == 0:
            raise ValueError()
        e = Estimator(self._lm)
        eid = id(e)
        self._estimators[eid] = e

        resp.data = json.dumps(
            {'eid': eid}
        ).encode('utf-8')
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_201
        return

    def __getitem__(self, arg: int) -> Estimator:
        return self._estimators[arg]


class EIDResouce:
    _root: RootResource

    def __init__(self, root_resource: RootResource) -> None:
        self._root = root_resource

    def on_post(self, req: Request, resp: Response, *, eid: int) -> None:
        try:
            key_str = req.params['key']
        except Exception:
            raise Exception(req.params)

        klass = TagWord if TagWord.is_include(key_str) else int
        key: Key = Key([klass(key_str)])

        self._root[eid].add(key)
        words = self._root[eid].result

        if words is None:
            raise Exception('Estimator has no result')

        resp.data = json.dumps({
            'eid': eid,
            'result': Word.to_str(words),
        }).encode('utf-8')
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200

    def on_get(self, req: Request, resp: Response, *, eid: int) -> None:
        self._root[eid].finish()

        words = self._root[eid].result

        if words is None:
            raise Exception()

        resp.data = json.dumps({
            'id': eid,
            'result': Word.to_str(words)
        }).encode('utf-8')

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200


root = RootResource()
eid_resource = EIDResouce(root)

api = API(middleware=[CORSMiddleware()])

api.req_options.auto_parse_form_urlencoded = True

api.add_route('/', root)
api.add_route('/{eid:int}', eid_resource)
