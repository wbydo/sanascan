from .mapped_classes import(
    Base,
    Corpus,
    CorpusFile,
    CorpusData,
    SentenceDelimiter
    # Sentence,
    # SplitMethod
)

class SNKException(Exception):
    pass

def init(engine):
    Base.prepare(engine, reflect=True)
