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
        self.storage = storage(self.N)
        self.data = [ None for i in range(self.N) ]
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
            nid = self.storage.AddNode()
            self.data.append(None)

        return self.GetNode(nid)

    def RemoveNode(self, node):
        nid = self._NodeId(node)
        self._IdGuard(nid)

        if nid == len(self.data) - 1:
            self.data.pop()
            self.storage.Remove()
        else:
            self.data[nid] = None
            self._unset.add(nid)

    def GetWeight(self, node1, node2):
        nid1 = self._NodeId(node1)
        nid2 = self._NodeId(node1)
        self._IdGuard(nid1)
        self._IdGuard(nid2)

        return self.storage.Get(nid1, nid2)

    def SetWeight(self, node1, node2, val):
        nid1 = self._NodeId(node1)
        nid2 = self._NodeId(node1)
        self._IdGuard(nid1)
        self._IdGuard(nid2)

        return self.storage.Set(nid1, nid2, val)

    def GetData(self, node):
        nid = self._NodeId(node)
        self._IdGuard(nid)
        return self.data[nid]

    def SetData(self, node, val):
        nid = self._NodeId(node)
        self._IdGuard(nid)
        self.data[nid] = val

    def __getitem__(self, indices):
        return self.GetNode(indices)

    def __len__(self):
        return len(self.storage) - len(self._unset)

    ###### Custom Methods #####

    def _NodeId(node):
        if node is None:
            raise TypeError("Node cannot be None")
        if isinstance(node, _Node):
            return node.nid
        if not isinstance(node, int):
            return int(node)
        return node

    def _IdGuard(nid):
        if nid not in self.storage or nid in self._unset:
            raise KeyError("Invalid node id: %s" % nid)




def _ensureStartId(startNode):
    if isinstance(startNode, _Node):
        return startNode.nid
    if not isinstance(startNode, int):
        return int(startNode)
    return startNode


class Graph2(object):
    def __init__(self, numnodes, directed=False, 
            storage=MatrixStorage):
        self.N = numnodes
        self.directed = directed

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
        self.N += 1
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
        if not isinstance(graph, GraphInterface):
            raise TypeError("Invalid graph: " % graph)
        self.graph = graph
        self.nid = nid

    def Connect(self, node, weight):
        return self.graph.SetWeight(self.nid, node, weight)

    def Weight(self, node):
        return self.graph.GetWeight(self.nid, nodeId)

    def Children(self):
        ids = self.graph.storage.GetChildren(self.nid)
        return [ self.graph[nid] for nid in ids ]

    def ChildIds(self):
        ids = self.graph.storage.GetChildren(self.nid)
        return list(ids)

    def Parents(self):
        ids = self.graph.storage.GetParents(self.nid)
        return [ self.graph[nid] for nid in ids ]

    def ParentIds(self):
        ids = self.graph.storage.GetParents(self.nid)
        return list(ids)

    def Get(self):
        return self.graph.GetData(self.nid)

    def Set(self, val):
        return self.graph.SetData(self.nid, val)

    def __getitem__(self, nid):
        return self.Weight(nid)




class _Node2(object):
    def __init__(self, graph, nid):
        self.graph = graph
        self.nid = nid

    def Connect(self, index, weight):
        return self.graph.Connect(self.nid, index, weight)

    def Children(self):
        ids = self.graph.storage.GetChildren(self.nid)
        return [ self.graph[nid] for nid in ids ]

    def ChildIds(self):
        ids = self.graph.storage.GetChildren(self.nid)
        return list(ids)

    def Parents(self):
        ids = self.graph.storage.GetParents(self.nid)
        return [ self.graph[nid] for nid in ids ]

    def ParentIds(self):
        ids = self.graph.storage.GetParents(self.nid)
        return list(ids)

    def Weight(self, nodeId):
        return self.graph.Weight(self.nid, nodeId)

    def Get(self):
        return self.graph.GetData(self.nid)

    def Set(self, val):
        return self.graph.SetData(self.nid, val)

    def __getitem__(self, nid):
        return self.Weight(nid)

