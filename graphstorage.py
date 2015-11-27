import numpy as np

class MatrixStorage(object):
    def __init__(self, N, directed):
        if not isinstance(N, int):
            raise Exception("Invalid first parameter")
        self.N = N
        self.matr = np.zeros((self.N, self.N))
        self._unset = set()

    # API methods:

    def GetWeight(self, n1, n2):
        self._EnsureNodeId(n1)
        self._EnsureNodeId(n2)
        return self.matr[n1,n2] 

    def SetWeight(self, n1, n2, weight):
        self._EnsureNodeId(n1)
        self._EnsureNodeId(n2)
        self.matr[n1,n2] = weight 

    def AddNode(self):
        if len(self._unset) == 0:
            self.Resize(self.N + 1)
            return self.N - 1
        anElem = next(iter(self._unset))
        self._unset.remove(anElem)
        return anElem

    def RemoveNode(self, nid):
        self._EnsureNodeId(nid)

        if nid == self.N - 1:
            self.Resize(nid)
            return

        self._unset.add(nid)
        self._ZeroOut(nid)

    def Resize(self, newN):
        islarger = newN > self.N
        self.N = newN
        if islarger:
            self._AdjustUp()
        else:
            self._AdjustDown()

    def GetChildren(self, nodeId):
        self._EnsureNodeId(nodeId)
        return (index for index, x in enumerate(self.matr[nodeId,:]) if x != 0)

    def GetParents(self, nodeId):
        self._EnsureNodeId(nodeId)
        return (index for index, x in enumerate(self.matr[:, nodeId]) if x != 0)

    def __len__(self):
        return self.N - len(self._unset)

    def __getitem__(self, indices):
        nfrom, nto = _IndexParse(indices)
        return self.GetWeight(nfrom, nto)

    def __setitem__(self, indices, val):
        nfrom, nto = _IndexParse(indices)
        return self.SetWeight(nfrom, nto, val)

    # Own methods

    def _EnsureNodeId(self, nid):
        if nid >= self.N or nid < 0 or nid in self._unset:
            raise KeyError("Invalid node id")

    def _AdjustUp(self):
        assert(self.matr.shape[0] < self.N)
        newA = np.zeros((self.N, self.N))
        newA[:self.matr.shape[0], :self.matr.shape[1]] \
            = self.matr
        self.matr = newA

    def _AdjustDown(self):
        assert(self.matr.shape[0] > self.N)
        newA = self.matr[:self.N, :self.N]
        self.matr = newA

    def _ZeroOut(self, nid):
        self.matr[nid,:] = 0
        self.matr[:,nid] = 0

 



class ListStorage(object):
    def __init__(self, N, directed):
        self.data = [ {} for i in range(N) ]
        self.directed = directed
        self._unset = set()

    # API Methods

    def GetWeight(self, n1, n2):
        self._EnsureNodeId(n1)
        self._EnsureNodeId(n2)
        
        if self.directed:
            if n1 > n2:
                x = n1; n1 = n2; n2 = x; 

        if n2 not in self.data[n1]:
            return 0
        return self.data[n1][n2]

    def SetWeight(self, n1, n2, weight):
        self._EnsureNodeId(n1)
        self._EnsureNodeId(n2)
        
        if self.directed:
            if n1 > n2:
                x = n1; n1 = n2; n2 = x; 

        self.data[n1][n2] = weight

    def AddNode(self):
        if len(self._unset) == 0:
            self.Resize(len(self.data) + 1)
            return len(self.data) - 1

        firstElt = next(iter(self._unset))
        self._unset.remove(firstElt)
        return firstElt

    def RemoveNode(self, nid):
        self._EnsureNodeId(nid)

        if nid == len(self.data) - 1:
            self.Resize(nid)
            return

        self._unset.add(nid)
        self._Sanitize(nid)

    def Resize(self, newN):
        current = len(self.data)
        if newN == current:
            return
        if newN < current:
            self._AdjustDown(newN)
        else:
            self._AdjustUp(newN)

    def GetChildren(self, nodeId):
        self._EnsureNodeId(nodeId)
        return (x for x in self.data[nodeId])

    def GetParents(self, nodeId):
        self._EnsureNodeId(nodeId)
        return (index for index, x in enumerate(self.data) if nodeId in x 
            and index not in self._unset)

    def __len__(self):
        return len(self.data) - len(self._unset)

    def __getitem__(self, indices):
        start, end = _IndexParse(indices)
        return self.GetWeight(start, end)
        
    def __setitem__(self, indices, val):
        start, end = _IndexParse(indices)
        return self.SetWeight(start, end, val)

    # Own methods

    def _EnsureNodeId(self, nid):
        if not isinstance(nid, int):
            raise TypeError("node id is of wrong type")

        if nid >= len(self.data) or nid < 0 \
                or nid in self._unset:
            raise KeyError("Invalid node id: " + str(nid))

    def _AdjustUp(self, N):
        assert(N > len(self.data))
        self.data.extend({} for i in range(len(self.data), N))

    def _AdjustDown(self, N):
        assert(N < len(self.data))
        self.data = self.data[:N]

        # Cleanse the dictionaries of now incorrect values
        possibleVals = range(N, len(self.data))
        self._Sanitize(possibleVals)

    def _Sanitize(self, nids):
        if isinstance(nids, int):
            nids = [ nids ]

        for d in self.data:
            for nid in nids:
                if nid in d:
                    del d[nid]

def _IndexParse(indices):
    if isinstance(indices, int):
        raise Exception("Must supply 2 indices")
    if isinstance(indices, tuple):
        if len(indices) != 2:
            raise Exception("Must supply 2 indices")
        return indices 
    if isinstance(indices, slice):
        return (indices.start, indices.stop)
    raise Exception("Unrecognized index parameters")

