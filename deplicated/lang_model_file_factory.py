import glob
import os
from itertools import tee

from hashlib import sha1

from sqlalchemy import func
from more_itertools import chunked

from anakin.lang_model.lang_model import LangModel
from anakin.lang_model.srilm import srilm

from anakin.db.model import Base, Sentence, LangModelFile
from anakin.db.session import database, engine_and_session

class CreateLangModelError(Exception):
    pass

class LangModelFileFactory():
    def __init__(self, database, max_get_size=500000, echo=True):
        self._ENGINE, self._Session = engine_and_session(database, echo)
        Base.prepare(self._ENGINE, reflect=True)

        self._max_get_size = max_get_size

    def _sentence_num(self):
        session = self._Session()
        i = session.query(Sentence.id).count()
        session.close()
        return i

    def _all_sentence_id(self):
        session = self._Session()
        for s in session.query(Sentence):
            yield s.id
        session.close()

    def _sentences_by_id(self, id_list):
        gen = chunked(id_list, self._max_get_size)
        for i in gen:
            session = self._Session()
            q = session.query(Sentence)\
                .filter(Sentence.id.in_(i))
            for j in q:
                yield j
            session.close()

    def get_lang_model_file(self, id_list, order):
        id_set = set(id_list)
        if not len(id_list) == len(id_set):
            raise CreateLangModelError('id_listに重複有り')

        # とりあえずarpaを生成
        _ = self._sentences_by_id(id_list)
        sentences1, sentences2 = tee(_)
        extract_contents = lambda sentence: sentence.contents

        wakati_text = '\n'.join(map(extract_contents, sentences1))
        arpa_binary = srilm(wakati_text, order).strip()

        h = sha1(arpa_binary)
        checksum = sha1(arpa_binary).digest()

        # 存在確認
        session = self._Session()
        q = session.query(LangModelFile)\
            .filter(LangModelFile.checksum == checksum)
        lmf = q.first()

        if lmf:
            if not id_set == set([s.id for s in lmf.sentences]):
                session.close()
                raise CreateLangModelError('checksumは一致するがidが一致しない')
            session.close()
            return lmf

        # 生成
        lmf = LangModelFile(
            order=order,
            contents=arpa_binary,
            checksum=checksum,
            sentences=list(sentences2)
        )
        session.add(lmf)
        session.commit()
        # session.close()

        return lmf
