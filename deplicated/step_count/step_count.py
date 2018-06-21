from collections import namedtuple
import numpy as np

from anakin.util.word import Word

Position = namedtuple('Position', ['cons', 'vow'])

class Step(namedtuple('Step', ['num'])):
    def __add__(self, other):
        return Step(num=(self.num + other.num))

_KATAKANA = [
    'アイウエオ',
    'カキクケコ',
    'サシスセソ',
    'タチツテト',
    'ナニヌネノ',
    'ハヒフヘホ',
    'マミムメモ',
    'ヤユヨ',
    'ラリルレロ',
    'ワヲンー'
]

_org = 'ヴァィゥェォガギグゲゴザジズゼゾッダヂヅデドバビブベボパピプペポャュョ'
_cov = 'ウアイウエオカキクケコサシスセソツタチツテトハヒフヘホハヒフヘホヤユヨ'

_CONV_TABLE = str.maketrans(_org, _cov)

_TRADITIONAL = np.array([range(i, i+5) for i in range(0,10)])

_PAIR_WISE = np.vstack([
    np.array([range(i, i+5) for i in range(0,5)]),
    np.array([range(i, i+5) for i in range(0,5)])
])

_COL_NUM_ALL = np.array([[i]*5 for i in range(0, 10)])

_COL_NUM_SQ = np.vstack([
    np.array([[i]*5 for i in range(0,3)]),
    np.array([[i]*5 for i in range(1,4)]),
    np.array([[i]*5 for i in range(2,5)]),
    np.array([3]*5)
])

METHODS = ['traditional', 'pair_wise', 'col_num_all', 'col_num_sq']

def _yomi2pos(words):
    yomi_only = ''.join([w.yomi for w in words if not w.yomi in Word.MARK.values()])
    clean = yomi_only.translate(_CONV_TABLE)

    def _mozi2pos(mozi):
        for idx, same_cons in enumerate(_KATAKANA):
            if not mozi in same_cons:
                continue
            cons = idx
            vow = same_cons.index(mozi)
            return Position(cons=cons, vow=vow)
        raise ValueError(f'[{mozi}]はない')
    return tuple(_mozi2pos(mozi) for mozi in clean)

def words2step(words, method=None):
    if method is None:
        raise ValueError('methodの指定がない')

    positions = _yomi2pos(words)

    def _pos2step(position, table):
        if position is None:
            return Step(num=0)
        
        vow = position.vow
        cons = position.cons
        num = table[cons][vow]
        return Step(num=num)

    def _total_steps(positions, table):
        steps = (_pos2step(pos, table) for pos in positions)
        return sum(steps, Step(num=0))

    if method == 'traditional':
        return _total_steps(positions, _TRADITIONAL)

    if method == 'pair_wise':
        return _total_steps(positions, _PAIR_WISE)

    if method == 'col_num_all':
        return _total_steps(positions, _COL_NUM_ALL)

    if method == 'col_num_sq':
        return _total_steps(positions, _COL_NUM_SQ)

    raise ValueError('methodの指定が想定外')


    positions = _yomi2pos(words)
