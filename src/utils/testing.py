from utils.general import *
from os import system

def testPath(pN,v):
    return formatPath(pN,v) + '/package/test'

def clone_lower_tests(packname,vL,vU):
    system('rm -r ./' + testPath(packname,vU))
    system('cp -r ./' + testPath(packname,vL) + ' ' + testPath(packname,vU))