import numpy as np
from graphstorage import MatrixStorage

def _ensureStartId(startNode):
    if isinstance(startNode, _Node):
        return startNode.nid
    if not isinstance(startNode, int):
        return int(startNode)
    return startNode


class Graph(object):
    def __init__(self, numnodes, directed=False, 
            storage=MatrixStorage):
        self.N = numnodes
        self.directed = directed

        # A = adjacency matrix, n x n
        #   A[i,j] > 0 if node i connects to node j through an edge
        #   A[i,j] = weight of edge
        self.storage = storage(self.N, self.directed)
        self.data = [ None for i in range(self.N) ]

    def GetNode(self, nodeIndex):
        if nodeIndex is None:
            raise TypeError("node index cannot be None")
        if not isinstance(nodeIndex, int):
            raise TypeError("node index is the wrong type")
        if nodeIndex >= self.N or nodeIndex < 0:
            raise KeyError()
        return _Node(self, nodeIndex)

    def AddNode(self):
        newId = self.storage.AddNode()
        self._ResizeData(self.N + 1)
        return self.GetNode(newId)

    def Resize(self, N):
        if N == self.N:
            return
        
        self.storage.Resize(N)
        self._ResizeData(N)
        self.N = N

    def Connect(self, index1, index2, weight):
        self.storage[index1, index2] = weight
        #if not self.directed:
        #    self.A[index2, index1] = weight

    def Weight(self, index1, index2):
        return self.storage[index1, index2]

    def GetData(self, index):
        return self.data[index]

    def SetData(self, index, val):
        self.data[index] = val

    def _ResizeData(self, newN):
        assert(self.N != newN)
        if self.N < newN:
            lenDiff = newN - self.N
            self.data.extend([ None for i in range(lenDiff) ])
        else:
            self.data = self.data[:self.N]
        
    ####### Overloads #######

    def __getitem__(self, nid):
        return self.GetNode(nid)

    def __len__(self):
        return len(self.storage)


class _Node(object):
    def __init__(self, graph, nid):
        self.graph = graph
        self.nid = nid

    def Connect(self, index, weight):
        return self.graph.Connect(self.nid, index, weight)

    def NeighborNodes(self):
        ids = _Node._NeighborsCore(self.graph, self.nid)
        return [ self.graph[nid] for nid in ids ]

    def NeighborIds(self):
        return list(_Node._NeighborsCore(self.graph, self.nid))

    def Weight(self, nodeId):
        return self.graph.Weight(self.nid, nodeId)

    def Get(self):
        return self.graph.GetData(self.nid)

    def Set(self, val):
        return self.graph.SetData(self.nid, val)

    @staticmethod
    def _NeighborsCore(graph, nid):
        return graph.storage.GetNeighbors(nid)

    def __getitem__(self, nid):
        return self.Weight(nid)

