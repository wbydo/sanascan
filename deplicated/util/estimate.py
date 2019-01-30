from anakin.util.key import Key
from anakin.util.key_to_word import yomi2tuple
from anakin.util.word import Word

class Node:
    def __init__(self, word, root=False):
        self._word = word
        if root:
            self._word = '<s>'
            self.sentence = '<s>'
            self.sentence_clean = '<s>'
            self.score = 0.0

    def _set_score(self, score):
        self.score = score

    def _set_parent(self, parent):
        self._parent = parent
        self.sentence = parent.sentence + ' ' + str(self._word)

        last = self._word.surface if not self._word == '</s>' else self._word
        self.sentence_clean = parent.sentence_clean + ' ' + last

    def search_parent(self, candidates, lang_model, order):
        scores = [self._calc_score(can, lang_model, order) for can in candidates]

        max_score = max(scores)
        self._set_score(max_score)

        parent = candidates[scores.index(max_score)]
        self._set_parent(parent)

    def _pick_up_by_order(self, words, order):
        words_list = words.split(' ')
        if len(words_list) <= order:
            return words

        else:
            return ' '.join(words_list[-order:])

    def _calc_score(self, other, lang_model, order):
        sentence = other.sentence + ' ' + str(self._word)
        words = self._pick_up_by_order(sentence, order)
        score = other.score + lang_model.score(words)

        return score

def estimate(words, key_to_word, lang_model, order):
    t = sum((yomi2tuple(w.yomi) for w in words),())
    key = Key(*t)

    root_node = Node('', root=True)

    l = len(key)
    wait_child = [[] for i in range(l+1)]
    wait_child[0].append(root_node)

    for i in range(l):
        if len(wait_child[i]) == 0:
            continue

        candidates = wait_child[i]
        for word, subkey in key_to_word.get_by_key(key, i):
            node = Node(word)
            node.search_parent(candidates, lang_model, order)

            j = len(subkey) + i
            wait_child[j].append(node)

    eos_node = Node('</s>')
    eos_node.search_parent(wait_child[l], lang_model, order)
    # return eos_node
    est_sentence = ' '.join(eos_node.sentence.split(' ')[1:-1])
    return Word.from_sentence(est_sentence)
