import traceback

class TestManager(object):
    _tests = []

def test(func):
    TestManager._tests.append(func)
    return func

def prefix(pref_func):
    def prefix_dec(actual_func):
        def executed(*args, **kwargs):
            data = pref_func()
            return actual_func(data, *args, **kwargs)
        executed.__name__ = actual_func.__name__
        return executed
    return prefix_dec

def run(tests=None):
    if tests == None:
        _do_run(TestManager._tests)
        return

    _do_run(tests)

def _do_run(tests):
    numToRun = len(tests)
    numPassed = 0
    for t in tests:
        success = _run_single(t)
        if success:
            numPassed += 1
    
    print('')
    print("==============================")
    print(numPassed, '/', numToRun, "successful")

def _run_single(testToRun):
    print("running:" + testToRun.__name__)
    try:
        testToRun()
        print("")
        return True
    except AssertionError:
        print("FAILURE")
    except:
        print traceback.format_exc() # print stacktrace

    return False
        

