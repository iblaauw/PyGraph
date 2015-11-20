import unittest
from unittest import TestSuite, TestCase
from ..graphstorage import MatrixStorage, ListStorage

class _StorageTestBase(TestCase):
    def setUp(self):
        self.storage = self.create(5, False) 
        self.storage.SetWeight(0, 1, 3)

    def test_init_len(self):
        self.assertEqual(len(self.storage), 5)

    def test_get(self):
        self.assertEqual(self.storage.GetWeight(0,1), 3)

    def test_get_bracket(self):
        self.assertEqual(self.storage[0,1], 3)

    def test_get_slice(self):
        self.assertEqual(self.storage[0:1], 3)

    def test_set(self):
        self.storage.SetWeight(1, 3, 7)
        self.assertEqual(self.storage[1,3], 7)
        self.assertNotEqual(self.storage[3,1], 7)

    def test_set_bracket(self):
        self.storage[1,3] = 7
        self.assertEqual(self.storage[1,3], 7)
        self.assertNotEqual(self.storage[3,1], 7)

    def test_set_slice(self):
        self.storage[1:3] = 7
        self.assertEqual(self.storage[1,3], 7)
        self.assertNotEqual(self.storage[3,1], 7)

    def test_addnode(self):
        nid = self.storage.AddNode()
        self.assertIsNotNone(nid)

        self.assertNotEqual(self.storage[0,nid], 3)
        self.assertNotEqual(self.storage[nid,0], 3)
        self.assertNotEqual(self.storage[1,nid], 3)
        self.assertNotEqual(self.storage[nid,1], 3)

        self.assertEqual(len(self.storage), 6)
    


class MatrixTest(_StorageTestBase):
    def create(self, *args, **kwargs):
        return MatrixStorage(*args, **kwargs)

class ListTest(_StorageTestBase):
    def create(self, *args, **kwargs):
        return ListStorage(*args, **kwargs)

test_classes = (MatrixTest, ListTest)

def load_tests(loader, standard_tests, unused):
    suite = TestSuite()
    for c in test_classes:
        tests = loader.loadTestsFromTestCase(c)
        suite.addTest(tests)
    return suite

if __name__ == "__main__":
    unittest.main()

