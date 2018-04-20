from subprocess import Popen
from subprocess import STDOUT
from subprocess import PIPE

def srilm(wakati, order):
    with Popen(['ngram-count', '-text', '-', '-order', str(order), '-unk', '<unk>'], stdout=PIPE, stdin=PIPE) as pros:
        s = wakati.encode()
        count = pros.communicate(s)[0].strip()

    with Popen(['ngram-count', '-order', str(order), '-read', '-', '-lm', '-', '-unk', '<unk>'], stdout=PIPE, stdin=PIPE) as pros:
        arpa = pros.communicate(count)[0].strip().decode()

    return  arpa
