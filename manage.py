from migrate.versioning.shell import main

from anakin.constants import DATABASE

if __name__ == '__main__':
    main(
        debug='False',
        url = DATABASE,
        repository='./anakin/db/migrate'
    )
