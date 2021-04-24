# Python Imports
from os import listdir
from os.path import isfile, join

# Obtain the contents of a file as a single string
def get_file_contents(filename):
    contents = None
    with open(filename, "r") as f:
        contents = f.read()
    return contents

# Obtain a list of the relatve path of every js file contained in the given directory
def get_all_js_files(directory):
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    directories = [d for d in listdir(directory) if not isfile(join(directory, d))]

    js_files = []
    for f in files:
        if f[-3:] == ".js":
            js_files.append(join(directory, f))

    for d in directories:
        js_files.extend(get_all_js_files(join(directory, d)))

    return js_files