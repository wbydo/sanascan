import re

class BaseSentenceDelimiter:
    def _split(self, delimiter_regex, text):

        p = re.compile(delimiter_regex)

        sentences = [i.strip() for i in re.split(p, text) if i.strip()]
        length = len(sentences)

        for idx, sentence in enumerate(sentences):
            yield {
                'length': length,
                'nth': idx + 1,
                'text': sentence.strip(),
            }
