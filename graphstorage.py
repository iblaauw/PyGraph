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
    def Set(self, n1, n2, val): raise NotImplementedError

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
            self._IdGuardSingle(arg)

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
            return (indices.start, indices.stop)

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
        super(ListStorage, self).__init__(N)
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
        self.N -= 1
        self._Cleanse(self.N)
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



