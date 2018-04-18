import os
import glob

from sqlalchemy.dialects.mysql import insert

from setting import ENGINE, Base, File, Post, Session
from posts_extractor import PostsExtractor
from rakuten_travel_strategy import RakutenTravelStrategy

engine = ENGINE
Base.metadata.bind=engine

base = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(base, 'data'))

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
    conn = engine.connect()
    conn.execute(on_duplicate_key_stmt, posts)
