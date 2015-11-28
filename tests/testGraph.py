import unittest
from unittest import TestSuite, TestCase
from ..graph import Graph
from ..graphstorage import MatrixStorage, ListStorage

class _GraphTestBase(TestCase):
    def setUp(self):
        self.graph = self.create(5)
        self.graph.SetWeight(1,2,5)
        self.graph.SetData(3, 6)

    ###### Custom Assert Funcs ######

    def assert_access_eq(self, i, j, val):
        g = self.graph
        self.assertEqual(g.GetWeight(i,j), val)
        self.assertEqual(g[i].Weight(j), val)
        self.assertEqual(g[i][j], val)

    def assert_data_eq(self, i, val):
        g = self.graph
        self.assertEqual(g.GetData(i), val)
        self.assertEqual(g[i].Get(), val)

    def assert_access_fail(self, i, j):
        g = self.graph
        with self.assertRaises(KeyError):
            _ = g.GetWeight(i,j)
        with self.assertRaises(KeyError):
            _ = g[i][j]
        with self.assertRaises(KeyError):
            _ = g[i].Weight(j)

    def assert_data_fail(self, i):
        g = self.graph
        with self.assertRaises(KeyError):
            _ = g.GetData(i)
        with self.assertRaises(KeyError):
            _ = g[i].Get()


    ###### Tests ###################
    
    def test_init_len(self):
        self.assertEqual(len(self.graph), 5)

    def test_get(self):
        self.assert_access_eq(1,2,5)
        self.assert_access_eq(1,0,0)
        self.assert_access_eq(0,1,0)
        self.assert_access_eq(3,4,0)

    def test_out_range(self):
        self.assert_access_fail(-1, 1)
        self.assert_access_fail(1, -1)
        self.assert_access_fail(2, 7)
        self.assert_access_fail(4, 5)
        self.assert_access_fail(8, 1)
        self.assert_access_fail(-2, 6)

        self.assert_data_fail(-1)
        self.assert_data_fail(-3)
        self.assert_data_fail(5)
        self.assert_data_fail(7)

    def test_node_creation(self):
        g = self.graph
        n0 = g[0]
        n1 = g[1]
        n3 = g[3]

        self.assertEqual(n0.nid, 0)
        self.assertEqual(n1.nid, 1)
        self.assertEqual(n3.nid, 3)

        self.assertTrue(n0.graph is g)
        self.assertTrue(n1.graph is g)
        self.assertTrue(n3.graph is g)

    def test_data(self):
        g = self.graph

        self.assert_data_eq(0,None)
        self.assert_data_eq(1,None)
        self.assert_data_eq(4,None)

        g.SetData(2,3)
        g[3].Set("hi")

        self.assert_data_eq(2,3)
        self.assert_data_eq(3,"hi")

        g[2].Set(None) # Should not error

    def test_add_node(self):
        g = self.graph
        node = g.AddNode()
        self.assertIsNotNone(node)

        nid = node.nid

        self.assertIsNotNone(nid)

        self.assertEqual(len(g), 6)

        self.assert_access_eq(nid, 0, 0)
        self.assert_access_eq(nid, 1, 0)
        self.assert_access_eq(nid, 4, 0)
        self.assert_access_eq(0, nid, 0)
        self.assert_access_eq(1, nid, 0)
        self.assert_access_eq(4, nid, 0)

        self.assert_data_eq(nid, None)

        g[nid].Connect(4, -1)

        self.assert_access_eq(nid, 4, -1)

    def test_remove_node(self):
        g = self.graph
        g.SetWeight(1,2,4)
        g.SetWeight(2,3,3)

        g.RemoveNode(1)

        self.assert_access_fail(0,1)
        self.assert_access_fail(1,2)
        self.assert_access_fail(1,4)

        with self.assertRaises(KeyError):
            g.SetWeight(1,3, 4)

        self.assert_access_eq(2,3,3)

    def test_add_remove(self):
        g = self.graph
        node = g.AddNode()

        g.SetWeight(node, 3, 4)
        g.SetWeight(4, node, 3)
        g.SetWeight(1,3,2)

        g.RemoveNode(node)

        self.assert_access_fail(node.nid, 3)
        self.assert_access_fail(node.nid, 4)
        self.assert_access_fail(4, node.nid)
        self.assert_access_fail(1, node.nid)
        self.assert_access_eq(1,3,2)

    def test_invalid_node(self):
        g = self.graph
        node = g[1]
        g.RemoveNode(1)

        with self.assertRaises(KeyError):
            node.Connect(3, 4)
        with self.assertRaises(KeyError):
            _ = node.Weight(3)
        with self.assertRaises(KeyError):
            _ = node.Children()
        with self.assertRaises(KeyError):
            _ = node.ChildIds()
        with self.assertRaises(KeyError):
            _ = node.Parents()
        with self.assertRaises(KeyError):
            _ = node.ParentIds()
        with self.assertRaises(KeyError):
            _ = node.Get()
        with self.assertRaises(KeyError):
            node.Set(5)
        with self.assertRaises(KeyError):
            _ = node[4]

    def test_children(self):
        g = self.graph
        self.assertIsInstance(g[1].Children(), list)

        x = [ n.nid for n in g[1].Children() ]
        y = [ n.nid for n in g[2].Children() ]
        z = [ n.nid for n in g[3].Children() ]

        self.assertEqual(x, [ 2 ])
        self.assertEqual(y, [])
        self.assertEqual(z, [])

    def test_childids(self):
        g = self.graph
        self.assertIsInstance(g[1].ChildIds(), list)

        x = g[1].ChildIds()
        y = g[2].ChildIds()
        z = g[3].ChildIds()

        self.assertEqual(x, [ 2 ])
        self.assertEqual(y, [])
        self.assertEqual(z, [])

    def test_parents(self):
        g = self.graph

        self.assertIsInstance(g[2].Parents(), list)
        self.assertIsInstance(g[2].ParentIds(), list)

        x = [ n.nid for n in g[2].Parents() ]
        y = [ n.nid for n in g[1].Parents() ]
        z = [ n.nid for n in g[3].Parents() ]

        self.assertEqual(x, [ 1 ])
        self.assertEqual(y, [])
        self.assertEqual(z, [])

    def test_parentids(self):
        g = self.graph
        self.assertIsInstance(g[2].ParentIds(), list)

        x = g[2].ParentIds()
        y = g[1].ParentIds()
        z = g[3].ParentIds()

        self.assertEqual(x, [ 1 ])
        self.assertEqual(y, [])
        self.assertEqual(z, [])

    def test_use_node_for_ops(self):
        pass


class MatrGraphTest(_GraphTestBase):
    def create(self, size):
        return Graph(size, False, storage=MatrixStorage)

class ListGraphTest(_GraphTestBase):
    def create(self, size):
        return Graph(size, False, storage=ListStorage)

test_classes = (MatrGraphTest, ListGraphTest)

def load_tests(loader, standard_tests, unused):
    suite = TestSuite()
    for c in test_classes:
        tests = loader.loadTestsFromTestCase(c)
        suite.addTest(tests)
    return suite

