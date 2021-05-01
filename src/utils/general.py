from os import *

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

# Obtain the contents of a file as a single string
def get_file_contents(filename):
    contents = None
    with open(filename, "r") as f:
        contents = f.readlines()
    return contents

# Get the old version v1 of a file, and the new version v2
def get_two_versions(packname, v1, v2):
    get_pkg_src(packname,v1)
    get_pkg_src(packname,v2)

def formatPath(packname,version):
    return f'{packname}/{packname}-{version}'

'''
    Get the package src
    YES THIS IS SUBJECT TO TAKEOVER AS THE INPUT IS NOT PARSED
    NO I'M NOT GOING TO SANITIZE THE INPUTS
'''
def get_pkg_src(packname,version):
    fpath = formatPath(packname,version)
    tarPath = './temp/' + fpath + '.tgz'
    system('mkdir -p ./temp/' + fpath)
    system('wget $(npm v ' + packname + '@' + version + ' dist.tarball) -O  ' + tarPath)
    system("tar -xvzf " + tarPath + " -C ./temp/" + fpath + " && rm " + tarPath)