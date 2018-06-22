import os
import sys
import fnmatch

path_ = os.path.abspath(
    os.path.dirname(__file__))
sys.path.insert(0, path_)

import util

if __name__ == '__main__':
    util.insert_splitter('Splitter001')

    session = util.Session()
    od = (
        session.query(util.db.OriginalData)
            .filter(util.db.OriginalData.id == 49).one())

    sp = session.query(util.db.Splitter).one()

    session.close()


    import time
    start = time.time()

    for _ in range(30):
        list(sp.split(od.contents))

    elapsed_time = time.time() - start
    print()
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    print()
    print()
