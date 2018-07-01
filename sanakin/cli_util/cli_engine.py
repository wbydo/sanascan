import argparse

from ..err import NotImplementException
from .db_api import sessionmaker_

class SNKCLIEngine(argparse.ArgumentParser):
    def __init__(self, description):
        super(__class__, self).__init__(
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        self.add_argument('CONFIG', help='config.yml')
        self.add_argument(
            '-E', '--environment',
            default='develop',
            help='DB環境の指定(default: develop)'
        )

        self.default_group = self.add_mutually_exclusive_group()
        self.default_group.add_argument(
            '-d', '--delete',
            action='store_true',
            help=f'RTURのすべてのデータを削除'
        )

        self.default_group.add_argument(
            '-a', '--all',
            action='store_true',
            help=f'RTURのすべてのデータをinsert'
        )

        self.default_group.add_argument(
            '-s', '--sandbox',
            action='store_true',
            help='挙動確認用'
        )

    def confirm(self, msg='do it?'):
        def decorator(f):
            def wrapper(*args, **kwargs):
                f(*args, **kwargs)
            return wrapper

        while True:
            ans = input('[{}]{}[Y/n] '.format(
                self._args.environment,
                msg
            ))
            if ans in ['Y', 'n']:
                break
        if ans == 'Y':
            return decorator
        else:
            return lambda f: lambda *args, **kwargs: None

    def _delete_mode(self, session):
        raise NotImplementException()

    def _sandbox_mode(self, session):
        raise NotImplementException()

    def _insert_mode(self, session, *, is_develop_mode=True):
        raise NotImplementException()

    def run(self):
        self._args = self.parse_args()
        Session = sessionmaker_(self._args.CONFIG, self._args.environment)

        if self._args.delete:
            with Session() as s:
                self._delete_mode(s)

        elif self._args.sandbox:
            with Session() as s:
                self._sandbox_mode(s)

        else:
            is_develop_mode = not self._args.all
            with Session() as s:
                self._insert_mode(s, is_develop_mode=is_develop_mode)
