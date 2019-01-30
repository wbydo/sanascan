class Key():
    def __init__(self, *args):
        # if not all([isinstance(i,int) for i in args]):
        #     raise TypeError

        self._tpl = tuple(args)

    def __eq__(self, other):
        if not isinstance(other, Key):
            raise TypeError
        return self._tpl == other._tpl

    def __hash__(self):
        return hash(self._tpl)

    def __repr__(self):
        return '<Key {}>'.format(repr(self._tpl))

    def subsequence(self, start):
        # if not isinstance(start, int):
        #     raise TypeError

        if start >= len(self._tpl):
            raise ValueError

        l = len(self._tpl)
        for i in range(start+1, l+1):
            subtpl = self._tpl[start:i]
            yield Key(*subtpl)

    def __len__(self):
        return len(self._tpl)
