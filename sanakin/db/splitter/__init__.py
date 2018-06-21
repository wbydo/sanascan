from ... import SNKException

def _split_function(splitter_name):
    if not splitter_name == 'Splitter001':
        raise SNKException(
            f'splitter_name: {splittername}')

    return __hello_world

def __hello_world(multi_sentence):
    for i in range(10):
        yield 'Hello World'
