from utils.testing import *
from utils.general import *
from os import system, chdir, getcwd
from os.path import isdir, isfile
from collections import OrderedDict

import json

# REQUIREMENT IS THAT THE TEST FOLDER IS NAMED "TEST" NOTHING MORE NOTHING LESS

def run_tests(packname,vL,vU):
    basedir = getcwd()
    system('rm -f' + packname + '/testResult*.json')
    lPath = '/' + formatPath(packname,vL) + "/package"
    uPath = '/' + formatPath(packname,vU) + "/package"

    chdir(basedir + lPath)
    print(getcwd())
    system('jest --all --silent --json --outputFile=../../testResultL.json -c=jest.config.json')

    chdir(basedir + uPath)
    print(getcwd())
    system('jest --all --silent --json --outputFile=../../testResultU.json -c=jest.config.json')

def compare_results(package):
    if not isfile('testResultL.json') or not isfile('testResultU.json'):
        return 3, []
    lRes = json.loads(open('testResultL.json','r').read(),object_pairs_hook=OrderedDict)
    uRes = json.loads(open('testResultU.json','r').read(),object_pairs_hook=OrderedDict)

    diff = []
    # No need to compare total test count,
    ltres = lRes["testResults"]
    utres = uRes["testResults"]
    ltres.sort(key=lambda x:x['name'])
    utres.sort(key=lambda x:x['name'])

    i = 0
    while i < len(ltres):
        curTests = None
        curL = [(s['fullName'], s['status']) for s in ltres[i]['assertionResults']]
        curU = [(s['fullName'], s['status']) for s in utres[i]['assertionResults']]
        curTests = list(zip(curL,curU))
        i+= 1

        for test in curTests:
            # print(test)
            if test[0][1] != test[1][1]:
                diff.append((test[0][0],(test[0][1],test[1][1])))
    
    if lRes['numPassedTests'] != uRes['numPassedTests'] or lRes['numPassedTestSuites'] != uRes['numPassedTestSuites']:
        return 2, diff
    elif len(diff) != 0:
        return 1, diff
    else:
        return 0, diff

# Return values are below
# retcode, data
# Data can be a message, or it can be the test differences
def compare_tests(package,vL,vU, debug=False):
    basedir = getcwd()
    load_two_versions(package,vL,vU)
    clone_lower_tests(package,vL,vU)
    run_tests(package,vL,vU)
    chdir(basedir + '/' + package)
    retcode, diff = compare_results(package)
    if retcode != 0:
        if debug:
            print(f"!! Versions {vL} and {vU} differ!!\nERRCODE: {retcode}\n[(funcName,(old,new))]")
            print(diff)
    else:
        if debug:
            print(f"Tests indicate versions {vL} and {vU} are identitlcal\nTo further confirm this check code coverage of the tests in {vL}, update for better coverage, and run again")
    return retcode, diff

def get_version_list(packname, force=False):
    vListPath = getcwd() + '/' +  packname + '-verlist.json'
    ret = []
    if not force and isfile(vListPath):
        jLoad = json.loads(open(vListPath,'r').read())
        for v in jLoad:
            ret.append(v)
        return ret
    else:
        system('npm view ' + packname + ' versions --json >&1 > ' + vListPath)

        jLoad = json.loads(open(vListPath,'r').read())
        for v in jLoad:
            ret.append(v)
        return ret

def compare_all_tests(packname):
    vlist = []
    vlist = get_version_list(packname,force=False)
    print(vlist)
    vlist.sort()
    print(vlist)
    
    # compatMatrix = [[0 for i in xrange(M)] for j in xrange(M)]
    compatDict = {}
    for i in range(0,len(vlist)):
        vL = vlist[i]
        compatDict[vL] = []
        for j in range(i + 1, len(vlist) - 1):
            vU = vlist[j]
            print(f'Comparing {vL} and {vU}')
            retcode,diff = compare_tests(packname,vL,vU)
            
            #Checking for compatible only
            if retcode == 0:
                compatDict[vL].append(vU)
    print(compatDict)
    return compatDict

if __name__ == '__main__':
    checkTemp()
    print("Package Name: ",end='')
    pname = input()
    
    '''print("Lower Version: ",end='')
    vL = input()
    print("Higher Version: ",end='')
    vU = input()'''

    compare_all_tests(pname)

    #compare_tests(pname,vL,vU)
    #compare_results('naev-npm','1.3.1','1.3.2')