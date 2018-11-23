from typing import Dict
from pathlib import Path
import json

from falcon import API, MEDIA_JSON, Request, Response
from falcon import HTTP_200, HTTP_201, HTTP_204

from .estimator import Estimator
from .lang_model import LangModel
from .word import Word, TagWord
from .key import Key


class Resource:
    _estimators: Dict[int, Estimator]
    _lm: LangModel

    def __init__(self) -> None:
        self._estimators = {}

        # あとで変更
        with (Path.home() / 'arpa/LM0006.txt').open() as f:
            self._lm = LangModel(f.read())

    def on_post(self, req: Request, resp: Response) -> None:
        e = Estimator(self._lm)
        id_ = id(e)
        self._estimators[id_] = e

        resp.data = json.dumps(
            {'id': id_}
        ).encode('utf-8')
        resp.content_type = MEDIA_JSON
        resp.status = HTTP_201

    def on_put(self, req: Request, resp: Response) -> None:
        id_ = int(req.params['id'])
        key_str = req.params['key']

        klass = TagWord if TagWord.is_include(key_str) else int
        key: Key = Key([klass(key_str)])

        self._estimators[id_].add(key)

        resp.status = HTTP_204

    def on_get(self, req: Request, resp: Response) -> None:
        id_ = int(req.params['id'])
        self._estimators[id_].finish()

        words = self._estimators[id_].result

        if words is None:
            raise Exception()

        resp.data = json.dumps({
            'id': id_,
            'result': Word.to_str(words)
        }).encode('utf-8')

        resp.content_type = MEDIA_JSON
        resp.status = HTTP_200


api = API()
resource = Resource()
api.add_route('/', resource)
