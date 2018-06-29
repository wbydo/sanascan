from .mapped_classes import(
    Base,
    Corpus,
    CorpusFile,
    CorpusData,
    # Sentence,
    # SplitMethod
)

def init(engine):
    Base.prepare(engine, reflect=True)
