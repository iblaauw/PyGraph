import unittest
from . import testStorage, testGraph, testIter

_allModules = (testStorage, testGraph, testIter)

def runAll():
    for mod in _allModules:
        runModule(mod)

def runModule(module):
    print('')
    print("#~~~~~~~~#OO#~~~~~~~~#0#~~~~~~~~#OO#~~~~~~~~#")
    print("Running test set %s:" % module.__name__)
    print("#~~~~~~~~#OO#~~~~~~~~#0#~~~~~~~~#OO#~~~~~~~~#")
    unittest.main(module=module, verbosity=2, exit=False)
