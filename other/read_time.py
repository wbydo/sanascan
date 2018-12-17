from pathlib import Path
import pickle
import time

from sanascan_backend.lang_model import LangModel


def stop_watch(msg):
    def decorater(func):
        def wrapper():
            start = time.time()
            func()
            finish = time.time()
            print(f'{msg}: {finish - start}')

        return wrapper
    return decorater


@stop_watch('テキストファイルの読み込み時間')
def text_file():
    with (Path.home() / 'arpa/LM0006.txt').open() as f:
        lm = LangModel(f.read())


@stop_watch('arpaファイルの読み込み時間')
def arpa_file():
    with (Path.home() / 'arpa/LM0006.pickle').open('rb') as f:
        lm = pickle.load(f)

if __name__ == '__main__':
    text_file()
    arpa_file()
