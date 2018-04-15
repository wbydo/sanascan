import re

from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import insert

from natto import MeCab

from setting import ENGINE, Base, Post, Sentence
from cleaner import Cleaner

def iter_sentence(session, cleaner, mecab):
    blank_ = re.compile(r'^\W*$')
    for post in session.query(Post).all():
        for sentence in cleaner.clean(post.contents, mecab):
            sentence_str = ' '.join(map(str, sentence))
            if not blank_.match(sentence_str):
                print(sentence_str)
                yield {'contents':sentence_str, 'post_id':post.id, 'post_file_id':post.file_id}

engine = ENGINE
Base.metadata.bind=engine

Session = sessionmaker(bind=engine)
session = Session()

cleaner = Cleaner()

with engine.begin() as conn, MeCab() as me:
    sentences = iter_sentence(session, cleaner, me)
    insert_stmt = insert(Sentence)
    on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
        contents=insert_stmt.inserted.contents
    )
    conn.execute(on_duplicate_key_stmt, list(sentences))
