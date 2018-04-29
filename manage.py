from migrate.versioning.shell import main
from anakin.db.session import database

from env import LOCAL

if __name__ == '__main__':
    main(
        debug='False',
        url = database(**LOCAL),
        repository='./anakin/db/migrate'
    )
