import re

from sqlalchemy.dialects.mysql import insert

from natto import MeCab

from setting import ENGINE, Base, Post, Sentence, Session
from cleaner import Cleaner

def iter_sentence(cleaner, mecab, max=None):
    blank_ = re.compile(r'^\W*$')
    session = Session()
    i = 0
    for post in session.query(Post).all():
        for sentence in cleaner.clean(post.contents, mecab):
            sentence_str = ' '.join(map(str, sentence))
            if not blank_.match(sentence_str):
                if not max is None and i >= max:
                    raise StopIteration()

                print(sentence_str)
                i += 1
                yield {'contents':sentence_str, 'post_id':post.id, 'post_file_id':post.file_id}

engine = ENGINE
Base.metadata.bind=engine

cleaner = Cleaner()

with engine.begin() as conn, MeCab() as me:
    sentences = iter_sentence(cleaner, me, 1000)
    insert_stmt = insert(Sentence)
    on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
        contents=insert_stmt.inserted.contents
    )
    conn.execute(on_duplicate_key_stmt, list(sentences))
