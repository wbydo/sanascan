from typing import Dict
from pathlib import Path
import json
import pickle

from falcon import API, MEDIA_JSON, Request, Response
from falcon import HTTP_200, HTTP_201
from jaconv import hira2kata

from .estimator import Estimator
from .lang_model import LangModel
from .word import TagWord, Sentence
from .key import Key
from .yomi_property import ColNum, Position


class CORSMiddleware:
    def process_request(self, req: Request, resp: Response) -> None:
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header(
                'Access-Control-Allow-Methods',
                'GET,POST,PUT,DELETE,OPTIONS')


class RootResource:
    _estimators: Dict[int, Estimator]
    _lm: LangModel

    def __init__(self) -> None:
        self._estimators = {}

        # あとで変更
        with (Path.home() / 'arpa/LM0006.pickle').open('rb') as f:
            self._lm = pickle.load(f)

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
            mode = req.params['mode']
        except Exception:
            raise Exception(req.params)

        key: Key
        if TagWord.is_include(key_str):
            key = Key([TagWord(key_str)])
        elif mode == 'normal':
            key = Key([Position(hira2kata(key_str))])
        elif mode == 'proposal':
            key = Key([ColNum(int(key_str))])
        else:
            raise Exception(f'mode: {mode}')

        self._root[eid].add(key)
        words = self._root[eid].result

        if words is None:
            raise Exception('Estimator has no result')

        sentence = Sentence.from_iter(words)

        resp.data = json.dumps({
            'eid': eid,
            'result': sentence.format_surfaces(),
        }).encode('utf-8')
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200

    def on_get(self, req: Request, resp: Response, *, eid: int) -> None:
        self._root[eid].finish()

        words = self._root[eid].result

        if words is None:
            raise Exception()

        sentence = Sentence.from_iter(words)

        resp.data = json.dumps({
            'id': eid,
            'result': sentence.format_surfaces(),
        }).encode('utf-8')

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200

    def on_delete(self, req: Request, resp: Response, *, eid: int) -> None:
        self._root[eid].reset()
        words = self._root[eid].result

        if words is not None:
            raise Exception()

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200


root = RootResource()
eid_resource = EIDResouce(root)

api = API(middleware=[CORSMiddleware()])

api.req_options.auto_parse_form_urlencoded = True

api.add_route('/', root)
api.add_route('/{eid:int}', eid_resource)
