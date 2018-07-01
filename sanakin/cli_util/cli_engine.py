import argparse

from ..err import SNKException
from .db_api import sessionmaker_

class SNKCLIEngine(argparse.ArgumentParser):
    def __init__(self, description, *, del_msg=None):
        super(__class__, self).__init__(
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        self._del_msg = del_msg

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

    def run(self):
        for mode in ['delete_mode', 'sandbox_mode', 'insert_mode']:
            if not hasattr(self, mode):
                raise SNKException(f'{mode}が実装されていない')

        args = self.parse_args()
        Session = sessionmaker_(args.CONFIG, args.environment)

        if args.delete:
            while True:
                ans = input(f'{self._del_msg}を削除しますか？[Y/n] ')
                if ans in ['Y', 'n']:
                    break

            if ans == 'Y':
                with Session() as s:
                    self.delete_mode(s)

        elif args.sandbox:
            with Session() as s:
                self.sandbox_mode(s)

        else:
            is_develop_mode = not args.all
            with Session() as s:
                self.insert_mode(s, is_develop_mode=is_develop_mode)
