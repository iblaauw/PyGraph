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
