from .node import Node


class DPMatching:
    def __init__(self, ref_words, est_words):
        self._max_x = len(ref_words) - 1
        self._max_y = len(est_words) - 1

        self._ref_words = ref_words
        self._est_words = est_words

        self._nodes = {}

        self.end_node = self.get_node(self._max_x, self._max_y)
        self.score = self.end_node.score

    def get_node(self, x, y):
        if x > self._max_x or y > self._max_y:
            raise ValueError()

        pos = (x, y)
        if pos in self._nodes:
            return self._nodes[pos]

        is_root = True if x == 0 and y == 0 else False
        node = Node(
            x=pos[0],
            y=pos[1],
            ref=self._ref_words[x],
            est=self._est_words[y],
            dpm=self,
            root=is_root
        )
        self._nodes[pos] = node
        return node

    def nodes(self):
        e = self.end_node
        while(not e.is_root):
            yield e
            e = e.parent
        yield e
