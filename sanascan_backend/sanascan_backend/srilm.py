from typing import IO

from subprocess import run

from tempfile import NamedTemporaryFile


def create_count_file(
        wakati: IO[str],
        order: int,
        delete: bool
        ) -> IO[str]:

    count_file = NamedTemporaryFile(
            'wt+',
            encoding='utf-8',
            delete=delete)

    cmd1 = [
            'ngram-count',
            '-unk', '<unk>',
            '-order', str(order),
            '-sort',
            '-text', wakati.name,
            '-write', count_file.name]

    run(cmd1)
    count_file.seek(0)
    return count_file


# def srilm(wakati: IO[str], order: int) -> IO[str]:
#     count_file = NamedTemporaryFile('wt+', encoding='utf-8')
#
#     cmd1 = [
#         'ngram-count',
#         '-unk', '<unk>',
#         '-order', str(order),
#         '-sort',
#         '-text', wakati.name,
#         '-write', count_file.name
#     ]
#     run(cmd1)
#     count_file.seek(0)
#
#     lm_file = NamedTemporaryFile('wt+', encoding='utf-8')
#     cmd2 = [
#         'ngram-count',
#         '-unk', '<unk>'
#         '-order', str(order),
#         '-read', count_file.name,
#         '-lm', lm_file.name,
#     ]
#     run(cmd2)
#     lm_file.seek(0)
#     return lm_file
