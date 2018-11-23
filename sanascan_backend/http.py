from typing import Dict
from pathlib import Path
import json

from falcon import API, MEDIA_JSON, HTTP_201, Request, Response

from .estimator import Estimator
from .lang_model import LangModel


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


api = API()
resource = Resource()
api.add_route('/', resource)
