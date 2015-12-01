import numpy as np
from graphstorage import MatrixStorage
from abc import ABCMeta, abstractmethod

class GraphInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def GetNode(self, nodeIndex): raise NotImplementedError

    @abstractmethod
    def AddNode(self): raise NotImplementedError

    @abstractmethod
    def RemoveNode(self, node): raise NotImplementedError

    @abstractmethod
    def GetWeight(self, node1, node2): raise NotImplementedError

    @abstractmethod
    def SetWeight(self, node1, node2, val): raise NotImplementedError

    @abstractmethod
    def GetData(self, node): raise NotImplementedError

    @abstractmethod
    def SetData(self, node, val): raise NotImplementedError

    @abstractmethod
    def __getitem__(self, indices): raise NotImplementedError

    @abstractmethod
    def __len__(self): raise NotImplementedError





class Graph(GraphInterface):
    def __init__(self, numnodes, directed=False, 
            storage=MatrixStorage):
        self.directed = directed
        self.storage = storage(numnodes)
        self.data = [ None for i in range(numnodes) ]
        self._unset = set()

    ###### Interface Methods #####

    def GetNode(self, nodeIndex):
        if nodeIndex is None:
            raise TypeError("node id cannot be None")
        if not isinstance(nodeIndex, int):
            raise TypeError("node id must be an int")
        self._IdGuard(nodeIndex)
        return _Node(self, nodeIndex)

    def AddNode(self):
        if len(self._unset) > 0:
            nid = self._unset.pop()
            self.storage.Zero(nid)
        else:
            nid = len(self.data)
            self.storage.AddNode()
            self.data.append(None)

        return self.GetNode(nid)

    def RemoveNode(self, node):
        nid = Graph._NodeId(node)
        self._IdGuard(nid)

        if nid == len(self.data) - 1:
            self.data.pop()
            self.storage.Remove()
        else:
            self.data[nid] = None
            self._unset.add(nid)

    def GetWeight(self, node1, node2):
        nid1 = Graph._NodeId(node1)
        nid2 = Graph._NodeId(node2)
        self._IdGuard(nid1)
        self._IdGuard(nid2)

        return self.storage.Get(nid1, nid2)

    def SetWeight(self, node1, node2, val):
        nid1 = Graph._NodeId(node1)
        nid2 = Graph._NodeId(node2)
        self._IdGuard(nid1)
        self._IdGuard(nid2)

        self.storage.Set(nid1, nid2, val)

    def GetData(self, node):
        nid = Graph._NodeId(node)
        self._IdGuard(nid)
        return self.data[nid]

    def SetData(self, node, val):
        nid = Graph._NodeId(node)
        self._IdGuard(nid)
        self.data[nid] = val

    def __getitem__(self, indices):
        return self.GetNode(indices)

    def __len__(self):
        return len(self.storage) - len(self._unset)

    ###### Custom Methods #####

    @staticmethod
    def _NodeId(node):
        if node is None:
            raise TypeError("Node cannot be None")
        if isinstance(node, _Node):
            return node.nid
        if not isinstance(node, int):
            return int(node)
        return node

    def _IdGuard(self, nid):
        if nid not in self.storage or nid in self._unset:
            raise KeyError("Invalid node id: %s" % nid)




class _Node(object):
    def __init__(self, graph, nid):
        if not isinstance(graph, GraphInterface):
            raise TypeError("Invalid graph: " % graph)
        self.graph = graph
        self.nid = nid

    def Connect(self, node, weight):
        return self.graph.SetWeight(self.nid, node, weight)

    def Weight(self, node):
        return self.graph.GetWeight(self.nid, node)

    def Children(self):
        self.graph._IdGuard(self.nid)
        ids = self.graph.storage.Children(self.nid)
        return [ self.graph[nid] for nid in ids ]

    def ChildIds(self):
        self.graph._IdGuard(self.nid)
        ids = self.graph.storage.Children(self.nid)
        return list(ids)

    def Parents(self):
        self.graph._IdGuard(self.nid)
        ids = self.graph.storage.Parents(self.nid)
        return [ self.graph[nid] for nid in ids ]

    def ParentIds(self):
        self.graph._IdGuard(self.nid)
        ids = self.graph.storage.Parents(self.nid)
        return list(ids)

    def Get(self):
        return self.graph.GetData(self.nid)

    def Set(self, val):
        return self.graph.SetData(self.nid, val)

    def __getitem__(self, nid):
        return self.Weight(nid)


