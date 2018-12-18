from pathlib import Path
import pickle
import time

from sanascan_backend.lang_model import LangModel


def stop_watch(msg):
    def decorater(func):
        def wrapper(name):
            start = time.time()
            func(name)
            finish = time.time()
            print(f'{msg}: {finish - start}')

        return wrapper
    return decorater


@stop_watch('テキストファイルの読み込み時間')
def text_file(name):
    with (Path.home() / 'arpa' / name).with_suffix('.txt').open() as f:
        lm = LangModel(f.read())


@stop_watch('arpaファイルの読み込み時間')
def arpa_file(name):
    with (Path.home() / 'arpa' / name).with_suffix('.pickle').open('rb') as f:
        lm = pickle.load(f)


if __name__ == '__main__':
    for name in ['LM0006', 'LM0007', 'LM0008']:
        print(name)
        print('--------------------------------')
        text_file(name)
        arpa_file(name)
        print()
        print()
