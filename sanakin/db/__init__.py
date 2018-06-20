from .mapped_classes import(
    Base,
    Corpus,
    SNKFile,
    OriginalData,
    Sentence,
    Splitter
)

def init(engine):
    Base.prepare(engine, reflect=True)
