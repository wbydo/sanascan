import os
import glob

from sqlalchemy.orm import sessionmaker

from setting import ENGINE, Base, File

engine = ENGINE
Base.metadata.bind=engine

Session = sessionmaker(bind=engine)
session = Session()

base = os.path.dirname(os.path.abspath(__file__))
path = os.path.abspath(os.path.join(base, 'data/*'))

for name in map(os.path.basename, glob.iglob(path)):
    file = File()
    file.name = name

    q = session.query(File).filter_by(name=file.name)
    if not session.query(q.exists()).scalar():
        session.add(file)
        session.commit()
