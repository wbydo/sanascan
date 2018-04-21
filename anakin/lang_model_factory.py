import glob
import os

from sqlalchemy import func
from more_itertools import chunked

from anakin.lang_model.lang_model import LangModel
from anakin.lang_model.srilm import srilm

from anakin.db.session import ENGINE, Session
from anakin.db.model import Sentence, LangModelFile

class CreateLangModelError(Exception):
    pass

class LangModelFactory():
    def __init__(self, lang_model_dir, max_get_size=500000):
        self._dir = lang_model_dir
        self._max_get_size = max_get_size

    def _sentence_num(self):
        session = Session()
        return session.query(Sentence.id).count()

    def _all_sentence_id(self):
        session = Session()
        for s in session.query(Sentence):
            yield s.id

    def _sentences_by_id(self, id_list):
        gen = chunked(id_list, self._max_get_size)
        for i in gen:
            session = Session()
            q = session.query(Sentence)\
                .filter(Sentence.id.in_(i))
            for j in q:
                yield j
            session.close()

    def _create_lang_model_without_existence_check(self, id_list, order):
        sentences = self._sentences_by_id(id_list)
        extract_contents = lambda sentence: sentence.contents

        wakati_text = '\n'.join(map(extract_contents, sentences))
        arpa_text = srilm(wakati_text, order).strip()

        return arpa_text

    def _write_lang_model_file(self, file_name, arpa_text):
        pattern = os.path.join(self._dir, '*')
        if file_name in map(os.path.basename, glob.iglob(pattern)):
            raise LangModelFileExistError()

        with open(os.path.join(self._dir, file_name), 'w') as f:
            f.write(arpa_text)

    def _insert_lang_model_to_db(self, file_name, id_list, order):
        sentences = list(self._sentences_by_id(id_list))
        lm = LangModelFile(name=file_name, sentences=sentences, order=order)

        session = Session()
        session.add(lm)
        session.commit()
        session.close()

        return lm

    def get_lang_model(self, id_list, order, file_name=None):
        id_set = set(id_list)
        if not len(id_list) == len(id_set):
            raise CreateLangModelError('id_listに重複有り')

        session = Session()
        for lm in session.query(LangModelFile):
            if id_set == set(s.id for s in lm.sentences)\
                and order == lm.order:
                session.close()
                return lm

        session.close()

        if file_name is None:
            raise CreateLangModelError('file_nameの指定がない')

        arpa_text = self._create_lang_model_without_existence_check(id_list, order)
        self._write_lang_model_file(file_name, arpa_text)
        lm = self._insert_lang_model_to_db(file_name, id_list, order)
        return lm
