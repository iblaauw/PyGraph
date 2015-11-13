from graph import Graph

def Tree():
    g = Graph(1, True)
    return _TreeNode(g, None)


class _TreeNode(object):
    def __init__(self, graph, parent):
        self.graph = graph
        self.parent = parent
        
        if parent == None:
            self.root = None
        elif parent.root == None:
            self.root = parent
        else:
            self.root = parent.root

        self.children = []
        self.label = None
        self.nid = len(graph) - 1

    def IsRoot(self):
        return self.root == None
    
    def GetChild(self, index):
        return self.children[index]

    def GetWeight(self, index):
        child = self.GetChild(index)
        return self.graph[self.nid][child.nid]

    def AddChild(self, weight=1):
        self.graph.AddNode()

        child = _TreeNode(self.graph, self)

        self.graph.Connect(self.nid, child.nid, weight)
        self.children.append(child)

        return child

    def SetWeight(self, index, weight):
        child = self.GetChild(index)

        self.graph.Connect(self.nid, child.nid, weight)

    def __getitem__(self, index):
        return self.GetChild(index)

    def __str__(self):
        r = " (root)" if self.IsRoot() else ''
        msg = "Node %d%s:\n" % (self.nid, r)

        pid = "None" if self.parent == None else str(self.parent.nid)
        msg += "\tparent: %s" % pid

        cids = (str(n.nid) for n in self.children)
        msg += "\tchildren: %s" % ' '.join(cids)

        return msg



