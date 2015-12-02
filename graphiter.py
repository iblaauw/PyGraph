from .graph import _Node
from collections import deque


def bfsiter(startNode):
    return _generaliter(startNode, True)

def dfsiter(startNode):
    return _generaliter(startNode, False)

def _generaliter(startNode, isbfs):
    if not isinstance(startNode, _Node):
        raise TypeError("bfsiter must be given a starting node.")
    getfunc = deque.popleft if isbfs else deque.pop
    return _doiter(startNode, getfunc)

def _doiter(startNode, getfunc):
    if not isinstance(startNode, _Node):
        raise TypeError("bfsiter must be given a starting node.")

    visited = set()
    frontier = deque()
    frontier.append(startNode)

    while True:
        if len(frontier) <= 0:
            break

        node = getfunc(frontier)
        if node.nid in visited:
            continue

        visited.add(node.nid)
        yield node

        for n in node.Children():
            if n.nid not in visited:
                frontier.append(n)


