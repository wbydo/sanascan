import os
import glob

from sqlalchemy.dialects.mysql import insert

from setting import ENGINE, Base, File

engine = ENGINE
Base.metadata.bind=engine

base = os.path.dirname(os.path.abspath(__file__))
path = os.path.abspath(os.path.join(base, 'data/*'))

file_names = [{'name':name} for name in map(os.path.basename, glob.iglob(path))]
insert_stmt = insert(File)
on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
    name=insert_stmt.inserted.name
)
conn = engine.connect()
conn.execute(on_duplicate_key_stmt, file_names)
