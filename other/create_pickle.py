import pickle
from pathlib import Path
from sanascan_backend.lang_model import LangModel


def create_pickle(name):
    print(f'start for {name}')
    txt_path = (Path.home() / 'arpa' / name).with_suffix('.txt')
    with txt_path.open() as f:
        lm = LangModel(f.read())

    print(f'finish reading {name}.txt')
    print(f'start dumping')

    pickle_path = (Path.home() / 'arpa' / name).with_suffix('.pickle')
    with pickle_path.open('wb') as f:
        pickle.dump(lm, f)

    print()


if __name__ == '__main__':
    for name in ['LM0007', 'LM0008']:
        create_pickle(name)
