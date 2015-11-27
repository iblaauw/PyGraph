import unittest
from unittest import TestSuite, TestCase
from ..graphstorage import MatrixStorage, ListStorage

class _StorageTestBase(TestCase):
    def setUp(self):
        self.storage = self.create(5, False) 
        self.storage.SetWeight(0, 1, 3)

    ######## Custom Assertion Functions #########

    def assert_access_fail(self, i, j):
        with self.assertRaises(KeyError):
            self.storage.GetWeight(i,j)
        with self.assertRaises(KeyError):
            self.storage[i,j]
        with self.assertRaises(KeyError):
            self.storage[i:j]

    def assert_access_eq(self, i, j, val):
        s = self.storage
        self.assertEqual(s.GetWeight(i,j), val)
        self.assertEqual(s[i,j], val)
        self.assertEqual(s[i:j], val)

    def assert_access_neq(self, i, j, val):
        s = self.storage
        self.assertNotEqual(s.GetWeight(i,j), val)
        self.assertNotEqual(s[i,j], val)
        self.assertNotEqual(s[i:j], val)

    ######## Tests ##############################

    def test_init_len(self):
        self.assertEqual(len(self.storage), 5)

    def test_get(self):
        self.assert_access_eq(0,1,3)
        self.assert_access_eq(1,0,0)
        self.assert_access_eq(0,0,0)
        self.assert_access_eq(4,4,0)

    def test_set(self):
        self.storage.SetWeight(1, 3, 7)
        self.assert_access_eq(1,3,7)
        self.assert_access_eq(3,1,0)

    def test_set_bracket(self):
        self.storage[1,3] = 7
        self.assert_access_eq(1,3,7)
        self.assert_access_eq(3,1,0)

    def test_set_slice(self):
        self.storage[1:3] = 7
        self.assert_access_eq(1,3,7)
        self.assert_access_eq(3,1,0)

    def test_addnode(self):
        nid = self.storage.AddNode()
        self.assertIsNotNone(nid)

        self.assert_access_eq(0,nid,0)
        self.assert_access_eq(nid,0,0)
        self.assert_access_eq(1,nid,0)
        self.assert_access_eq(nid,1,0)

        self.assertEqual(len(self.storage), 6)

    def test_out_of_range(self):
        self.assert_access_fail(-1,0)
        self.assert_access_fail(0,-1)
        self.assert_access_fail(5,0)
        self.assert_access_fail(0,5)
        self.assert_access_fail(13,-2)
        self.assert_access_fail(3,7)

    @unittest.skip("Undecided whether reflexive should fail or not")
    def test_get_reflexive(self):
        self.assert_access_fail(0,0)
        self.assert_access_fail(1,1)
        self.assert_access_fail(3,3)
    
    def test_add_then_set(self):
        nid = self.storage.AddNode()
        self.storage[2,nid] = 4
        self.assert_access_eq(2,nid,4)
        self.assert_access_neq(nid,2,4)

    def test_remove(self):
        self.storage.RemoveNode(1)

        self.assert_access_fail(0,1)
        self.assert_access_fail(3,1)
        self.assert_access_fail(1,0)
        
        self.assertEqual(len(self.storage), 4)
        self.assert_access_eq(3,4,0) 

    def test_add_remove(self):
        nid = self.storage.AddNode()
        
        self.storage[3,2] = 1
        self.storage[3,nid] = 4
        self.storage[nid,2] = 5

        self.storage.RemoveNode(nid)
        
        self.assert_access_fail(3, nid)
        self.assert_access_fail(nid, 2)
        self.assert_access_eq(3,2,1)

    def test_children(self):
        x = list(self.storage.GetChildren(0))
        self.assertIsNotNone(x)
        self.assertEqual(x, [ 1 ])

        y = list(self.storage.GetChildren(1))
        self.assertIsNotNone(y)
        self.assertEqual(y, [])

        z = list(self.storage.GetChildren(3))
        self.assertIsNotNone(z)
        self.assertEqual(z, [])

    def test_parents(self):
        x = list(self.storage.GetParents(1))
        self.assertIsNotNone(x)
        self.assertEqual(x, [ 0 ])

        y = list(self.storage.GetParents(0))
        self.assertIsNotNone(y)
        self.assertEqual(y, [])

        z = list(self.storage.GetParents(3))
        self.assertIsNotNone(z)
        self.assertEqual(z, [])

    def test_remove_children(self):
        self.storage.RemoveNode(1)
        x = list(self.storage.GetChildren(0))
        self.assertEqual(x, [])

    def test_remove_parents(self):
        self.storage.RemoveNode(0)
        x = list(self.storage.GetParents(1))
        self.assertEqual(x, [])



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

