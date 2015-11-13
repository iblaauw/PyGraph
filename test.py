from graph import *
from graphsearch import *
from tree import Tree
from graphstorage import *

matr = MatrixStorage(5, False)
#matr = ListStorage(5, False)

matr.SetWeight(0, 1, 3)

print matr.GetWeight(0, 1)

newid = matr.AddNode()

matr.SetWeight(2, newid, 7)

matr.RemoveNode(4)

matr.RemoveNode(newid)

newid2 = matr.AddNode()
print newid2

matr.SetWeight(2, newid2, 5)

try:
    matr.SetWeight(newid, newid2, 9)
    print "failed to detect out of range"
except:
    print "successfully out of range"

matr.SetWeight(1, newid2, 9)

matr.RemoveNode(1)

try:
    print matr[1:newid2]
    print "failed to detect out of range"
except:
    print "successfully out of range"

print len(matr)

print matr[2,4]
print matr[2:4]
print matr[4:2]

matr[4:2] = 3
print matr[4:2]


quit()


g = Graph(5, True)
g[0].Connect(1, 1)
g[0].Connect(2, 1)
g[1].Connect(3, 1)
g[1].Connect(2, 1)
g[2].Connect(4, 1)
g[3].Connect(4, 1)

for nid in bfsiter(g, 0):
    print nid

for nid in bfs_back_iter(g,0):
    print nid

for nid in dfsiter(g, 0):
    print nid

for nid in dfs_back_iter(g,0):
    print nid


t = Tree()
t.label = 'A'
print "is root: ", t.IsRoot()

child1 = t.AddChild()
print "child 1 id: ", child1.nid
print "child 1 parent: ", child1.parent.nid
print "child 1 root: ", child1.root.nid

child2 = child1.AddChild()
print "child 2 id: ", child2.nid
print "child 2 parent: ", child2.parent.nid
print "child 2 root: ", child2.root.nid

print t
print child1
print child2

quit()


x = Graph(5)
x.Connect(1,2,5)
print "A:", x.A

n = x[2]
print "n:", n

ids = n.NeighborIds()
print "ids:", ids

n.Connect(3, -1)

n2 = x[3]
print "Node 3:", n2

neighbors = n.NeighborNodes()
print "nodes:", neighbors
print "ids:", [ n.nid for n in neighbors ]

print x.A
print "weight:", x[3][2]

x = Graph(5, True)
x.Connect(1,2,5)
print "neighbors:", x[2].NeighborIds()
print "neighbors:", x[1].NeighborIds()
print "n2:", x[2][1]
print "n1:", x[1][2]

x.Resize(6)
print "A:", x.A

print x.data

x.Resize(3)
print "A:", x.A

print x.data

x.SetData(0, 25)
print "val:", x[0].Get()

x[1].Set(13)
print "val:", x.GetData(1)
