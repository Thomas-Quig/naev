from utils.testing import *
from utils.general import *
from os import *

# REQUIREMENT IS THAT THE TEST FOLDER IS NAMED "TEST" NOTHING MORE NOTHING LESS
def clone_lower_tests(packname,vL,vU):
    system('rm -r ./temp/' + testPath(packname,vU))
    system('cp ./temp' + testPath(packname(vL)) + ' ./temp' + formatPath(packname,vU))

def run_tests(packname,vL,vU):
    basedir = getcwd()
    lPath = './temp/' + formatPath(packname,vL)
    uPath = './temp/' + formatPath(packname,vU)

    chdir(lPath)
    system('jest --all --json --outputFile=../testResultL.json')

    chdir(basedir + uPath)
    system('jest --all --json --outputFile=../testResultU.json')

    
    

