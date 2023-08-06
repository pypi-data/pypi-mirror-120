import os
from .blob import TextBlob, Word, Sentence, Blobber, WordList

__version__ = '0.17.2'
__license__ = 'MIT'
__author__ = 'Prakash Dale'

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

__all__ = [
    'TextBlob',
    'Word',
    'Sentence',
    'Blobber',
    'WordList',
]
