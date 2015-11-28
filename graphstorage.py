import numpy as np
from abc import ABCMeta, abstractmethod


class StorageBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, N):
        if not isinstance(N, int):
            raise TypeError("Invalid N: %s" % N)
        self.N = N

    @abstractmethod
    def Get(self, n1, n2): raise NotImplementedError

    @abstractmethod
    def Set(self, n1, n2): raise NotImplementedError

    @abstractmethod
    def AddNode(self): raise NotImplementedError

    @abstractmethod
    def Remove(self): raise NotImplementedError

    @abstractmethod
    def Zero(self, nid): raise NotImplementedError

    @abstractmethod
    def Children(self, nid): raise NotImplementedError

    @abstractmethod
    def Parents(self, nid): raise NotImplementedError

    def __len__(self):
        return self.N

    def __getitem__(self, indices):
        start, end = self._ParseIndices(indices)
        return self.Get(start, end)

    def __setitem__(self, indices, val):
        start, end = self._ParseIndices(indices)
        return self.Set(start, end, val)

    def __contains__(self, nid):
        if not isinstance(nid, int):
            raise TypeError("Invalid node id type: %s" % type(nid))
        return nid >= 0 and nid < self.N

    def _IdGuard(self, *args):
        for arg in args:
            _IdGuardSingle(arg)

    def _IdGuardSingle(self, nid):
        if not isinstance(nid, int):
            raise TypeError("Invalid node id type: %s" % type(nid))
        if nid < 0 or nid >= self.N:
            raise KeyError("Invalid node id: %s" % nid)

    def _ParseIndices(self, indices):
        if isinstance(indices, int):
            raise IndexError("There must be 2 indices given")

        if isinstance(indices, tuple):
            if len(indices) != 2:
                raise IndexError("There must be 2 indices given")
            return indices

        if isinstance(indices, slice):
            return (indices.start, indices.finish)

        raise TypeError("Invalid indexing type given: %s" % type(nid))





class MatrixStorage(StorageBase):
    def __init__(self, N):
        super(MatrixStorage, self).__init__(N)
        self.matr = np.zeros((N, N))

    def Get(self, n1, n2):
        self._IdGuard(n1, n2)
        return self.matr[n1, n2]

    def Set(self, n1, n2, val):
        self._IdGuard(n1, n2)
        self.matr[n1, n2] = val

    def AddNode(self):
        newN = self.N + 1
        newMatr = np.zeros((newN, newN))
        newMatr[:self.N, :self.N] = self.matr

        self.N = newN
        self.matr = newMatr

    def Remove(self):
        self.N -= 1
        self.matr = self.matr[:self.N, :self.N]

    def Zero(self, nid):
        self._IdGuard(nid)
        self.matr[nid,:] = 0
        self.matr[:, nid] = 0

    def Children(self, nid):
        self._IdGuard(nid)
        return (i for i, x in enumerate(self.matr[nid, :]) if x != 0)

    def Parents(self, nid):
        self._IdGuard(nid)
        return (i for i, x in enumerate(self.matr[:, nid]) if x != 0)

    def __len__(self):
        assert(self.matr.shape[0] == self.N)
        return self.N





class ListStorage(StorageBase):
    def __init__(self, N):
        super(MatrixStorage, self).__init__(N)
        self.data = [ {} for i in range(N) ]

    def Get(self, n1, n2):
        self._IdGuard(n1, n2)
        if n2 not in self.data[n1]:
            return 0
        return self.data[n1][n2]

    def Set(self, n1, n2, val):
        self._IdGuard(n1, n2)
        self.data[n1][n2] = val

    def AddNode(self):
        self.data.append({})
        self.N += 1
        assert(len(self.data) == self.N)

    def Remove(self):
        self._Cleanse(nid)
        self.N -= 1
        self.data.pop()
        assert(len(self.data) == self.N)

    def Zero(self, nid):
        self._IdGuard(nid)
        self.data[nid] = {}
        self._Cleanse(nid)

    def Children(self, nid):
        self._IdGuard(nid)
        return iter(self.data[nid])

    def Parents(self, nid):
        self._IdGuard(nid)
        return (index for index, x in enumerate(self.data) if nid in x)

    def __len__(self):
        assert(len(self.data) == self.N)
        return self.N

    def _Cleanse(self, nid):
        for i in range(self.N):
            if nid in self.data[i]:
                del self.data[i][nid]





class MatrixStorage2(object):
    def __init__(self, N, directed):
        if not isinstance(N, int):
            raise TypeError("Invalid first parameter")
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

 



class ListStorage2(object):
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

