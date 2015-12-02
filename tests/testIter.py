import unittest
from unittest import TestSuite, TestCase
from ..graph import Graph
from ..graphiter import bfsiter, dfsiter

class _ShareTestBase(TestCase):
    def setUp(self):
        self.it = self.getIt()

    def assert_result(self, gen, correct):
        vals = [ n.nid for n in gen ]
        self.assertEqual(vals, correct)


    def test_invalid_input(self):
        graph = Graph(5, True)
        with self.assertRaises(TypeError):
            self.it(graph)
        with self.assertRaises(TypeError):
            self.it(None)
        with self.assertRaises(TypeError):
            self.it(5)

    def test_unconnected(self):
        graph = Graph(5, True)

        i = self.it(graph[1])
        self.assert_result(i, [1])
        i = self.it(graph[4])
        self.assert_result(i, [4])
        i = self.it(graph[0])
        self.assert_result(i, [0])

    def test_is_iterable(self):
        graph = Graph(5, True)
        i = self.it(graph[1])
        x = iter(i)

    def test_string(self):
        graph = Graph(5, True)
        graph.SetWeight(0, 1, 1)
        graph.SetWeight(1, 2, 1)
        graph.SetWeight(2, 3, 1)

        i = self.it(graph[0])
        self.assert_result(i, [ 0, 1, 2, 3 ])

    def test_loop(self):
        graph = Graph(5, True)
        graph.SetWeight(0, 1, 1)
        graph.SetWeight(1, 2, 1)
        graph.SetWeight(2, 0, 1)

        i = self.it(graph[0])
        self.assert_result(i, [ 0, 1, 2 ])

    def test_no_parents(self):
        graph = Graph(5, True)
        graph.SetWeight(0, 1, 1)
        graph.SetWeight(2, 1, 1)
        graph.SetWeight(3, 1, 1)

        i = self.it(graph[1])
        self.assert_result(i, [ 1 ])


class BfsTest(_ShareTestBase):
    def getIt(self):
        return bfsiter

    def test_simple(self):
        graph = Graph(5, True)
        graph.SetWeight(1,2,1)
        graph.SetWeight(1,3,1)
        graph.SetWeight(2,4,1)

        val = bfsiter(graph[1])
        self.assert_result(val, [ 1, 2, 3, 4 ])

    def test_child_order(self):
        graph = Graph(5, True)
        graph.SetWeight(1,2,1)
        graph.SetWeight(1,3,1)
        graph.SetWeight(1,4,1)

        val = bfsiter(graph[1])
        self.assert_result(val, [ 1, 2, 3, 4 ])


class DfsTest(_ShareTestBase):
    def getIt(self):
        return dfsiter

    def test_simple(self):
        graph = Graph(5, True)
        graph.SetWeight(1,2,1)
        graph.SetWeight(1,3,1)
        graph.SetWeight(3,4,1)

        val = dfsiter(graph[1])
        self.assert_result(val, [ 1, 3, 4, 2 ])

    def test_child_order(self):
        graph = Graph(5, True)
        graph.SetWeight(1,2,1)
        graph.SetWeight(1,3,1)
        graph.SetWeight(1,4,1)

        val = dfsiter(graph[1])
        self.assert_result(val, [ 1, 4, 3, 2 ])


test_classes = (BfsTest, DfsTest)

def load_tests(loader, standard_tests, unused):
    suite = TestSuite()
    for c in test_classes:
        tests = loader.loadTestsFromTestCase(c)
        suite.addTest(tests)
    return suite

