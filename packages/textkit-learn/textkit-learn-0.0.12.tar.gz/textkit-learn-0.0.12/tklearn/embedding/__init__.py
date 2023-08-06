from .loader import *
from .base import *
from tklearn.embedding import load_embedding

# noinspection SpellCheckingInspection
__all__ = [
    'WordEmbedding',
    'load_word2vec',
    'load_numberbatch',
    'load_embedding',
]


def load(d):
    """Loads embedding from provided parameter 'd'.

    Parameters
    ----------
    d Union[Dict, Text]
        Loads embedding from provided parameter 'd'

    Returns
    -------
        WordEmbedding
    """
    return load_embedding(d)
