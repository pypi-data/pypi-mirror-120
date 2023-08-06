from nltk.corpus import wordnet as wn

from tklearn.knowledge._base import KnowledgeGraph


class WordNet(KnowledgeGraph):
    def __init__(self):
        super(WordNet, self).__init__()

    def search(self, word):
        root = wn.synsets(word)
        return root
