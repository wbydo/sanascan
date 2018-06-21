from ... import SNKException

from . import splitter001

def _split_function(splitter_name):
    if not splitter_name == 'Splitter001':
        raise SNKException(
            f'splitter_name: {splittername}')

    return splitter001.split
