import unittest
from unittest import TestSuite, TestCase
from ..tree import TreeNode

class TreeTest(TestCase):
    def setUp(self):
        self.root = TreeNode()

    def assert_children(self, node, childids):
        val = [ c.nid for c in node.AllChildren() ]
        self.assertEqual(val, childids)

    def assert_node_eq(self, node1, node2):
        return self.assertEqual(node1.nid, node2.nid)

    def test_init(self):
        self.assertTrue(self.root.IsRoot())
        self.assertTrue(self.root.IsLeaf())
        self.assertEqual(len(self.root), 0)
        self.assert_children(self.root, [])
        self.assertIsNone(self.root.Parent())
        self.assert_node_eq(self.root.GetRoot(), self.root)

    def test_add_child(self):
        node = self.root.AddChild(5)

        self.assertEqual(len(self.root), 1)
        self.assertEqual(len(node), 0)

        self.assert_node_eq(self.root[0], node)
        self.assert_node_eq(self.root.GetChild(0), node)
        self.assert_node_eq(node.Parent(), self.root)

        self.assert_node_eq(node.GetRoot(), self.root)
        self.assertFalse(self.root.IsLeaf())
        self.assertTrue(node.IsLeaf())
        self.assertFalse(node.IsRoot())



test_classes = (TreeTest,)

def load_tests(loader, standard_tests, unused):
    suite = TestSuite()
    for c in test_classes:
        tests = loader.loadTestsFromTestCase(c)
        suite.addTest(tests)
    return suite
