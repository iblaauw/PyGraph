import unittest
from unittest import TestSuite, TestCase
from ..graph import Graph
from ..graphstorage import MatrixStorage, ListStorage

class _GraphTestBase(TestCase):
    def setUp(self):
        self.graph = self.create(5)
        self.graph.Connect(1,2,5)
        self.graph.SetData(3, 6)

    ###### Custom Assert Funcs ######

    def assert_access_eq(self, i, j, val):
        g = self.graph
        self.assertEqual(g.Weight(i,j), val)
        self.assertEqual(g[i].Weight(j), val)
        self.assertEqual(g[i][j], val)

    def assert_data_eq(self, i, val):
        g = self.graph
        self.assertEqual(g.GetData(i), val)
        self.assertEqual(g[i].Get(), val)

    def assert_access_fail(self, i, j):
        g = self.graph
        with self.assertRaises(KeyError):
            _ = g.Weight(i,j)
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

