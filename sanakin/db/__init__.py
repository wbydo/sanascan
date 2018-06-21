from .mapped_classes import(
    Base,
    Corpus,
    SKNFile,
    OriginalData,
    Sentence,
    SplitMethod
)

def init(engine):
    Base.prepare(engine, reflect=True)
