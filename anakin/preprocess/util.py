import os
import glob
import re

from natto import MeCab

from sqlalchemy.dialects.mysql import insert

from anakin.db.session import ENGINE, Session
from anakin.db.base import Base
from anakin.db.file import File
from anakin.db.post import Post
from anakin.db.sentence import Sentence

from anakin.preprocess.posts_extractor import PostsExtractor
from anakin.preprocess.rakuten_travel_strategy import RakutenTravelStrategy
from anakin.preprocess.cleaner import Cleaner

Base.metadata.bind=ENGINE

def insert_files():
    # pathの指定をコマンドラインから求めたほうが良いかも
    dirname_ = os.path.dirname(os.path.abspath(__file__))
    path = os.path.abspath(os.path.join(dirname_, '../../data/*'))

    file_names = [{'name':name} for name in map(os.path.basename, glob.iglob(path))]
    insert_stmt = insert(File)
    on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
        name=insert_stmt.inserted.name
    )

    conn = ENGINE.connect()
    conn.execute(on_duplicate_key_stmt, file_names)

def insert_posts():
    # pathの指定をコマンドラインから求めたほうが良いかも
    dirname_ = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(dirname_, '../../data'))

    session = Session()
    for file in session.query(File).all():
        path = os.path.join(data_dir, file.name)

        ext = PostsExtractor()
        strategy = RakutenTravelStrategy()

        posts = [dict(file_id=file.id, **e) for e in ext.apply(strategy, path)]
        insert_stmt = insert(Post)
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
            contents=insert_stmt.inserted.contents
        )
        conn = ENGINE.connect()
        conn.execute(on_duplicate_key_stmt, posts)

def insert_sentence(max):
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

    cleaner = Cleaner()
    with ENGINE.begin() as conn, MeCab() as me:
        sentences = iter_sentence(cleaner, me, max)
        insert_stmt = insert(Sentence)
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
            contents=insert_stmt.inserted.contents
        )
        conn.execute(on_duplicate_key_stmt, list(sentences))
