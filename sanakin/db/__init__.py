from .mapped_classes import(
    Base,
    Corpus,
    SNKFile,
    OriginalData,
    Sentence,
    SplitMethod
)

def init(engine):
    Base.prepare(engine, reflect=True)
