from utils.general import *
from os import system
from os.path import isdir

def testPath(pN,v):
    fpath = formatPath(pN,v)
    if isdir(fpath + '/package/test'):
        return fpath + '/package/test'
    elif isdir(fpath + '/package/tests'):
        return fpath + '/package/tests'
    elif isdir(fpath + '/package/__tests__'):
        return fpath + '/package/__tests__'
    elif isdir(fpath + '/package/__test__'):
        return fpath + '/package/__test__'
    else:
        print("ERROR: TESTS NOT FOUND")
        return None

def clone_lower_tests(packname,vL,vU):
    testPL = testPath(packname,vL)
    testPU = testPath(packname,vU)
    if testPL is None or testPU is None:
        return -1
    else:
        system('rm -r ' + testPU)
        system('cp -r ' + testPL + ' ' + testPU)
        return 0