from collections import deque
from graph import _Node, _ensureStartId

def bfsiter(graph, startNode):
    front = frontier(graph, startNode)
    while len(front) > 0:
        yield front.Peek()[0]
        front.Advance()

def bfs_back_iter(graph, startNode):
    front = frontier(graph, startNode)
    while len(front) > 0:
        yield front.Peek()
        front.Advance()

def dfsiter(graph, startNode):
    front = frontier(graph, startNode, isDfs=True)
    while len(front) > 0:
        yield front.Peek()[0]
        front.Advance()

def dfs_back_iter(graph, startNode):
    front = frontier(graph, startNode, isDfs=True)
    while len(front) > 0:
        yield front.Peek()
        front.Advance()


class frontier(object):
    def __init__(self, graph, startnode, isDfs=False):
        startid = _ensureStartId(startnode)
        self.q = deque([ (startid, None) ])
        self.reached = [ False for i in range(len(graph)) ]
        self.graph = graph
        self.isDfs = isDfs

    # function 1: removes node from queue and then pushes all
    #   its neighbors on - mark as reached
    # function 2: removes node from queue and ignores neighbors
    #   - not marked as reached
    # function 3: removes node from queue, ignores neighbors,
    #   marked as reached

    def Peek(self):
        return self.q[0]
    
    def Advance(self):
        nid, _ = self.q.popleft()

        self.reached[nid] = True

        neighbors = self.graph[nid].NeighborIds()
        filtered = (n for n in neighbors \
            if not self.reached[n])

        for node in filtered:
            if self.isDfs:
                self.q.appendleft( (node, nid) )
            else:
                self.q.append( (node, nid) )

        self._fix()
        
    def Remove(self):
        nid, _ = self.q.popleft()
        self.reached[nid] = True
        self._fix()

    def Ignore(self):
        self.q.popleft()
        self._fix()

    def _fix(self):
        while len(self.q) > 0 and self.reached[ self.q[0][0] ]:
            self.q.popleft()
        

    def __len__(self):
        return len(self.q)

