import glob
import os

from sqlalchemy import func
from more_itertools import chunked

from lang_model.lang_model import LangModel
from lang_model.srilm import srilm

from setting import ENGINE, Sentence, Session, LangModelFile

class CreateLangModelError(Exception):
    pass

class LangModelFactory():
    _base = os.path.dirname(os.path.abspath(__file__))
    _lm_dir = os.path.abspath(os.path.join(_base, 'lm'))
    _pattern = os.path.join(_lm_dir + '*')

    def __init__(self, max_get_size=500000):
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
        if file_name in map(os.path.basename, glob.iglob(LangModelFactory._pattern)):
            raise LangModelFileExistError()

        with open(os.path.join(LangModelFactory._lm_dir, file_name), 'w') as f:
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


# lmf = LangModelFactory()
# id_list = list(lmf._all_sentence_id())[:20]
# a = lmf.get_lang_model(id_list, order=3, file_name='test00555.arpa')
#
# id_list = list(lmf._all_sentence_id())[50:70]
# lmf.get_lang_model(id_list, order=3, file_name='test002.arpa')
# print(a)
