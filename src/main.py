# Python Imports
import os

# naev Imports
from utils.general import *
from utils.testing import *
from utils.static import *
from testsuite_compare import *
# 3rd Party Imports

def main():
	compare_tests('naev-npm','1.5.0','1.6.0',debug=True)
	
if __name__ == '__main__':
	main()
