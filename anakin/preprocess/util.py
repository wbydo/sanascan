import os
import glob
import re
from hashlib import sha1

from natto import MeCab

from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Load

from anakin.db.session import ENGINE, Session
from anakin.db.model import Base, File, Data, Sentence

from anakin.preprocess.cleaner import Cleaner

def register_single_file(file_path, dataset):
    file_name = os.path.basename(file_path)

    # f.read()でメモリリークしたら逐次読み込みを考える
    with open(file_path, 'rb') as f:
        contents = f.read()
        checksum = sha1().digest()

    session = Session()

    file = File(
        file_name=file_name,
        dataset=dataset,
        contents=contents,
        checksum=checksum
    )
    session.add(file)
    session.commit()
    session.close()

def extract_data():
    session = Session()
    query = session.query(File)\
        .options(Load(File).defer('contents'))
    for file in query:
        extractor = file.dataset.value.extractor

        datum= [dict(file_id=file.id, **e) for e in extractor(file.contents)]
        insert_stmt = insert(Data)
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
            contents=insert_stmt.inserted.contents
        )
        with ENGINE.begin() as conn:
            conn.execute(on_duplicate_key_stmt, datum)

def split_sentence(max):
    def iter_sentence(cleaner, mecab, max=None):
        blank_ = re.compile(r'^\W*$')
        session = Session()
        i = 0
        for data in session.query(Data).all():
            for sentence in cleaner.clean(data.contents, mecab):
                sentence_str = ' '.join(map(str, sentence))
                if not blank_.match(sentence_str):
                    if not max is None and i >= max:
                        raise StopIteration()

                    print(sentence_str)
                    i += 1
                    yield {'contents':sentence_str, 'data_id':data.id, 'data_file_id':data.file_id}

    cleaner = Cleaner()
    with ENGINE.begin() as conn, MeCab() as me:
        sentences = iter_sentence(cleaner, me, max)
        insert_stmt = insert(Sentence)
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
            contents=insert_stmt.inserted.contents
        )
        conn.execute(on_duplicate_key_stmt, list(sentences))
