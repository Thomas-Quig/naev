from utils.general import *
from os import system, getcwd
from os.path import isdir

def testPath(pN,v):
    fpath = formatPath(pN,v) + '/package'
    system('ls ' + fpath)
    if isdir(fpath + '/test'):
        return '/test'
    elif isdir(fpath + '/tests'):
        return '/tests'
    elif isdir(fpath + '/__tests__'):
        return '/__tests__'
    elif isdir(fpath + '/__test__'):
        return '/__test__'
    else:
        print("ERROR: TESTS NOT FOUND")
        return None
 
def setup_testing(packname,vL,vU):
    testPL = getcwd() + '/' + packname + '/curLowVer'
    testPU = getcwd() + '/' + packname + '/curHighVer'
    system('rm -rf ' + testPL + ' ' + testPU)
    system('cp -r ' + formatPath(packname,vL) + '/package' + ' ' + testPL)
    system('cp -r ' + formatPath(packname,vU) + '/package' + ' ' + testPU)
    
    testLoc = testPath(packname,vL)
    if testLoc is None:
        return -1
    else:
        system('rm -r ' + testPU + testLoc)
        system('cp -r ' + testPL + testLoc + ' ' + testPU)
        return 0