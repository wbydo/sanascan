from anakin.preprocess import util
from anakin.db.session import database

from env import LOCAL

if __name__ == '__main__':
    db = database(**LOCAL)

    util.extract_data(db)
    util.split_sentence(1000, db)
