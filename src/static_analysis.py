# Python Imports
from os import listdir
from os.path import isfile, join

# naev Imports
from utils/utils import *

# 3rd Party Imports

# This function analyzes the code of two versions of the same package to attempt to determine
# if they are functionally equivalent. It analyzes them according to this rubric:
# - We only check something if it is exported both when it is initially defined, and in the index.js file. If there is not an index.js file in the root package directory, we will check things exported when they are initially defined from any file in the root directory or the src directory. 
# - Classes
#     - We check that classes exported in the lower version are also exported in the higher version
#     - properties
#         - We ignore properties whose name is prefixed with '_' or '#'
#         - We check that all non-static properties declared at the top of the class in the lower version are still present in the higher version
#         - We check that all static properties declared at the top of the class in the lower version are still present in the higher version
#         - We check that any property of the form 'this.*' on the left side of an assignment in any function in the lower version is still present in the higher version
#     - functions
#         - we ignore functions whose name is prefixed with '_' or '#'
#         - We check that all required parameters are the same across both versions
# - Variables
#     - We check that variables exported in the lower version are also exported in the higher version
# - Functions
#     - We check that functions exported in the lower version are also exorted in the higher version
#     - We check that all required parameters are the same across both versions.
# @param lower_version_directory The root directory of the lower package version
# @param higher_version_directory The root directory of the higher package version
# @return This function returns a tuple of the form ((A, a), (B, b), (C, c), (D, d) (E, e)) where each letter represents a type of thing that was checked.
# The upper case letters represent the total number of that type of thing that were analyzed, while the lowercase letters represent the number of that type 
# of thing that were detected as different. A = clsses, B = class properties, C = class functions, D = variables, E = functions
def compare(lower_version_directory, higher_version_directory):