from utils.testing import *
from utils.general import *
from os import system, chdir, getcwd
from os.path import isdir, isfile
from collections import OrderedDict

import json

# REQUIREMENT IS THAT THE TEST FOLDER IS NAMED "TEST" NOTHING MORE NOTHING LESS

def run_tests(packname,vL,vU):
    basedir = getcwd()
    assert(basedir.split('/')[-1] == packname)
    system('rm -f ' + basedir + '/testResult*.json')
    lPath = basedir + '/curLowVer'
    uPath = basedir + '/curHighVer'

    chdir(lPath)
    #print(getcwd())
    system('jest --all --silent --json --outputFile=../testResultL.json -c=jest.config.json')

    chdir(uPath)
    #print(getcwd())
    system('jest --all --silent --json --outputFile=../testResultU.json -c=jest.config.json')

    chdir(basedir)
    

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
def compare_tests(package,vL,vU, debug=False,refreshPackages=False):

    # Get base directory to ensure you are there at the end
    basedir = getcwd()

    # Load vL and vU
    load_two_versions(package,vL,vU,forceRefresh=refreshPackages)

    # If tests dont exist in vL, return as such
    if setup_testing(package,vL,vU) == -1:
        return 4, []

    
    # Otherwise, run the tests from inside /temp/packname and save the test results
    # into testResultL.json and testResultU.json in the packname folder
    chdir(basedir + '/' + package)
    run_tests(package,vL,vU)

    # Compare the results 
    retcode, diff = compare_results(package)

    if retcode != 0:
        if debug:
            print(f"!! Versions {vL} and {vU} differ!!\nERRCODE: {retcode}\n[(funcName,(old,new))]")
            print(diff)
    else:
        if debug:
            print(f"Tests indicate versions {vL} and {vU} are identitlcal\nTo further confirm this check code coverage of the tests in {vL}, update for better coverage, and run again")
    
    # Return to base directory and exit
    chdir(basedir)
    return retcode, diff

def get_version_list(packname, force=False):
    vListPath = normpath(getcwd()) + '/' +  packname + '-verlist.json'
    print(vListPath)
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

def compare_all_tests(packname,preload=True,refresh=False):
    vlist = []
    vlist = get_version_list(packname,force=False)

    vlist.sort()
    if(preload):
        load_src_from_vlist(packname,vlist,forceRefresh=refresh)
    # compatMatrix = [[0 for i in xrange(M)] for j in xrange(M)]
    compatDict = {}
    for i in range(0,len(vlist) - 1):
        vL = vlist[i]
        compatDict[vL] = []
        for j in range(i + 1, len(vlist)):
            vU = vlist[j]
            print(f'Comparing {vL} and {vU}')
            retcode,diff = compare_tests(packname,vL,vU,refreshPackages=(refresh and (not preload)))
            
            #Checking for compatible only
            if retcode == 0:
                compatDict[vL].append(vU)
            else:
                print(f'Error {retcode} occured while comparing {vL} and {vU}, check errlist')
    print(compatDict)
    return compatDict

def compare_sequential_tests(packname,preload=True,refresh=False):
    vlist = []
    vlist = get_version_list(packname,force=refresh)

    vlist.sort()
    if(preload and refresh):
        load_src_from_vlist(packname,vlist,forceRefresh=refresh)
    # compatMatrix = [[0 for i in xrange(M)] for j in xrange(M)]
    compatDict = {}
    for i in range(0,len(vlist) - 1):
        vL = vlist[i]
        compatDict[vL] = []
        vU = vlist[i + 1]
        print(f'Comparing {vL} and {vU}')
        retcode,diff = compare_tests(packname,vL,vU,refreshPackages=(refresh and (not preload)))
        
        #Checking for compatible only
        if retcode == 0:
            compatDict[vL].append(vU)
        else:
            print(f'Error {retcode} occured while comparing {vL} and {vU}, check errlist')
    print(compatDict)
    return compatDict

if __name__ == '__main__':
    checkTemp()
    '''print("Package Name: ",end='')
    pname = input()
    
    
    print("Lower Version: ",end='')
    vL = input()
    print("Higher Version: ",end='')
    vU = input()
    '''
    #print(compare_tests(pname,vL,vU,debug=True,refreshPackages=False))
    compare_all_tests('naev-npm',preload=False,refresh=False)
    #vlist = get_version_list(pname,force=True)
    #load_src_from_vlist(pname,vlist,forceRefresh=True)
    #compare_sequential_tests(pname,preload=False,refresh=False)