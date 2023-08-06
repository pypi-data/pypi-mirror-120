import networkx as nx


class KnowledgeGraph:
    def __init__(self):
        self._graph = nx.MultiDiGraph()
