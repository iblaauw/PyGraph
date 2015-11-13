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
        self.A = np.zeros((self.N, self.N))
        self.data = [ None for i in range(self.N) ]

    def GetNode(self, nodeIndex):
        if nodeIndex >= self.N or nodeIndex < 0:
            raise IndexError()
        return _Node(self, nodeIndex)

    def AddNode(self):
        self.Resize(self.N + 1)

    def Resize(self, N):
        if N == self.N:
            return
        
        direction = N < self.N
        self.N = N
        if direction:
            self._AdjustDown()
        else:
            self._AdjustUp()

    def Connect(self, index1, index2, weight):
        self.A[index1, index2] = weight
        if not self.directed:
            self.A[index2, index1] = weight

    def Weight(self, index1, index2):
        return self.A[index1, index2]

    def GetData(self, index):
        return self.data[index]

    def SetData(self, index, val):
        self.data[index] = val

    def _AdjustUp(self):
        assert(self.A.shape[0] < self.N)
        newA = np.zeros((self.N, self.N))
        newA[:self.A.shape[0], :self.A.shape[1]] = self.A
        self.A = newA
        lenDiff = self.N - len(self.data)
        self.data.extend([ None for i in range(lenDiff) ])

    def _AdjustDown(self):
        assert(self.A.shape[0] > self.N)
        newA = self.A[:self.N, :self.N]
        self.A = newA
        self.data = self.data[:self.N]

    ####### Overloads #######

    def __getitem__(self, nid):
        return self.GetNode(nid)

    def __len__(self):
        return self.N


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
        return ( i for i, weight in enumerate(graph.A[nid,:]) if weight != 0 )

    def __getitem__(self, nid):
        return self.Weight(nid)

