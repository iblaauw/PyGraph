from .graph import Graph
from .graphstorage import ListStorage
from abc import ABCMeta, abstractmethod


class  TreeNodeInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def IsRoot(self): raise NotImplementedError()

    @abstractmethod
    def IsLeaf(self): raise NotImplementedError()

    @abstractmethod
    def GetRoot(self): raise NotImplementedError()

    @abstractmethod
    def GetParent(self): raise NotImplementedError()

    @abstractmethod
    def GetChild(self, index): raise NotImplementedError()

    @abstractmethod
    def AllChildren(self): raise NotImplementedError()

    @abstractmethod
    def AddChild(self, weight): raise NotImplementedError()

    @abstractmethod
    def Delete(self, node): raise NotImplementedError()

    @abstractmethod
    def GetWeight(self, child): raise NotImplementedError()

    @abstractmethod
    def SetWeight(self, node, val): raise NotImplementedError()

    @abstractmethod
    def Detach(self): raise NotImplementedError()

    @abstractmethod
    def Attach(self, subtree): raise NotImplementedError()

    @abstractmethod
    def GetUnderlyingGraph(self): raise NotImplementedError()

    @abstractmethod
    def __len__(self): raise NotImplementedError()

    @abstractmethod
    def __getitem__(self, index): raise NotImplementedError()


class _TreeBundle(object):
    def __init__(self, graph, rootid):
        self.graph = graph
        self.rootid = rootid

class TreeNode(TreeNodeInterface):
    def __init__(self, bundle=None, nid=None):
        if bundle == None:
            graph = Graph(1, True, storage=ListStorage)
            self._bundle = _TreeBundle(graph, 0)
            self.nid = 0
        else:
            if nid == None:
                raise TypeError("node id was expected but not provided")
            self._bundle = bundle
            self.nid = nid

    def IsRoot(self):
        return self.nid == self._bundle.rootid

    def IsLeaf(self):
        return len(self._GraphNode().Children()) == 0

    def GetRoot(self): raise NotImplementedError()
        if self.IsRoot():
            return self
        return self._CreateNode(self._bundle.rootid)

    def GetParent(self):
        parents = self._GraphNode().Parents()

        if len(parents) == 0:
            return None

        assert(len(parents) == 1)
        pid = parents[0]

        return self._CreateNode(pid)


    def GetChild(self, index):
        cid = self._ChildId(index)
        return self._CreateNode(cid)

    def AllChildren(self):
        children = self._GraphNode().ChildIds()
        return map(self._CreateNode, children)

    def AddChild(self, weight):
        node = self._bundle.graph.AddNode()
        nid = node.nid
        self._bundle.graph.SetWeight(self.nid, nid, weight)
        return self._CreateNode(nid)

    def Delete(self): raise NotImplementedError()

    #TODO: add a way to get weight to parent from this
    def GetWeight(self, index):
        cid = self._ChildId(index)
        return self._bundle.graph.GetWeight(self.nid, cid)

    def SetWeight(self, node, val): raise NotImplementedError()

    def Detach(self): raise NotImplementedError()

    def Attach(self, subtree): raise NotImplementedError()

    def GetUnderlyingGraph(self):
        return self._bundle.graph

    def __len__(self):
        return len(self._GraphNode().ChildIds())

    def __getitem__(self, index):
        return self.GetChild(index)

    def _GraphNode(self):
        return self._bundle.graph[self.nid]

    def _CreateNode(self, nid):
        return TreeNode(bundle=self._bundle, nid=nid)

    def _ChildId(self, index):
        children = self._GraphNode().ChildIds()
        return children[index]





#class TreeInterface(object):
#    __metaclass__ = ABCMeta
#
#    @abstractmethod
#    def GetRoot(self): raise NotImplementedError()
#
#    @abstractmethod
#    def GetWeight(self, node1, node2): raise NotImplementedError()
#
#    @abstractmethod
#    def SetWeight(self, node1, node2, val): raise NotImplementedError()
#
#    @abstractmethod
#    def __getitem__(self, nid): raise NotImplementedError()
#
#
#
#class TreeNodeInterface(object):
#    __metaclass__ = ABCMeta
#
#    # attribute nid
#    # attribute tree
#
#    @abstractmethod
#    def IsRoot(self): raise NotImplementedError()
#
#    @abstractmethod
#    def GetChild(self, index): raise NotImplementedError()
#
#    @abstractmethod
#    def AddChild(self, weight): raise NotImplementedError()
#
#    @abstractmethod
#    def RemoveChild(self, node): raise NotImplementedError()
#
#    @abstractmethod
#    def GetWeight(self, child, weight): raise NotImplementedError()
#
#    @abstractmethod
#    def SetWeight(self, child, weight): raise NotImplementedError()
#
#    @abstractmethod
#    def CreateSubTree(self): raise NotImplementedError()
#
#    @abstractmethod
#    def __getitem__(self, indices): raise NotImplementedError()
#
#
#class Tree(TreeInterface):
#    def __init__(self, graph=None, rootId=None):
#        if graph == None:
#            self._graph = Graph(1, storage=ListStorage)
#            self._rootid = 0
#        else:
#            if not isinstance(graph, Graph):
#                raise TypeError("The given graph must be of type Graph")
#            if rootId == None:
#                raise TypeError("If a graph is specified, the root id also must be specified.")
#            if not isinstance(rootId, int):
#                raise TypeError("The given root id must be an int.")
#
#            self._graph = graph
#            self._rootid = rootId
#
#    def GetRoot(self):
#        return TreeNode(self._rootid, self)
#
#    def GetWeight(self, node1, node2):
#        n1 = self._ensureNodeId(node1)
#        n2 = self._ensureNodeId(node2)
#        return self._graph.GetWeight(n1, n2)
#
#    def SetWeight(self, node1, node2, val):
#        n1 = self._ensureNodeId(node1)
#        n2 = self._ensureNodeId(node2)
#        self._graph.SetWeight(n1, n2, val)
#
#    def __getitem__(self, nid):
#        if not isinstance(nid, int):
#            raise TypeError("Node id must be an integer: %s" % nid)
#        return TreeNode(nid, self)
#
#    def _ensureNodeId(self, node):
#        if isinstance(node, TreeNode):
#            return node.nid
#        if isinstance(node, int):
#            return node
#        try:
#            return int(node)
#        except TypeError:
#            raise TypeError("Invalid node or node id: %s" % nid)
#
#
#
#
#class TreeNode(TreeNodeInterface):
#    def __init__(self, nid, tree):
#        self.nid = nid
#        self.tree = tree
#
#    def IsRoot(self): raise NotImplementedError()
#
#    def GetChild(self, index): raise NotImplementedError()
#
#    def AddChild(self, weight): raise NotImplementedError()
#
#    def RemoveChild(self, node): raise NotImplementedError()
#
#    def GetWeight(self, child, weight): raise NotImplementedError()
#
#    def SetWeight(self, child, weight): raise NotImplementedError()
#
#    def CreateSubTree(self): raise NotImplementedError()
#
#    def __getitem__(self, indices): raise NotImplementedError()
#
#
#
#
#def Tree():
#    g = Graph(1, True, storage=ListStorage)
#    return _TreeNode(g, None)
#
#
#
#class TreeNode(object):
#    def __init__(self, graph, parent):
#        self.graph = graph
#        self.parent = parent
#        self.nid = nid
#
#        if parent == None:
#            self.root = None
#        elif parent.root == None:
#            self.root = parent
#        else:
#            self.root = parent.root
#
#        _childids = graph[self.nid].ChildIds()
#        self.children = graph[self.nid].ChildIds()
#
#        self.nid = len(graph) - 1
#
#    def IsRoot(self):
#        return self.root == None
#
#    def GetWeight(self, index):
#        child = self.GetChild(index)
#        return self.graph[self.nid][child.nid]
#
#    def GetChild(self, index):
#        pass
#
#    def AddChild(self, weight=1):
#        self.graph.AddNode()
#
#        child = _TreeNode(self.graph, self)
#
#        self.graph.Connect(self.nid, child.nid, weight)
#        self.children.append(child)
#
#        return child
#
#    def SetWeight(self, index, weight):
#        child = self.GetChild(index)
#
#        self.graph.SetWeight(self.nid, child.nid, weight)
#
#    def __getitem__(self, index):
#        return self.GetChild(index)
#
#    def __str__(self):
#        r = " (root)" if self.IsRoot() else ''
#        msg = "Node %d%s:\n" % (self.nid, r)
#
#        pid = "None" if self.parent == None else str(self.parent.nid)
#        msg += "\tparent: %s" % pid
#
#        cids = (str(n.nid) for n in self.children)
#        msg += "\tchildren: %s" % ' '.join(cids)
#
#        return msg


