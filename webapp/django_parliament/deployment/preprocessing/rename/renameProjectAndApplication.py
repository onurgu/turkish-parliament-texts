import sys
import os

def replaceTextInDjangoFiles(projpath, oldtext, newtext):

    xfiles = [];xdirs = [];
    for (dirpath, dirnames, filenames) in os.walk(projpath):
        xfiles.extend(filenames)
        xdirs.extend(dirnames)
        if(".git" in xdirs): xdirs.remove(".git")
        break

    for xfile in xfiles:
        replaceTextInFile(projpath+"/"+xfile, oldtext, newtext)

    for xdir in xdirs:
        replaceTextInDjangoFiles(projpath+"/"+xdir, oldtext, newtext)


def replaceTextInFile(file_absolute_path, oldtext, newtext):
    with open(file_absolute_path, 'r') as f:
        filedata = f.read()    

    filedata = filedata.replace(oldtext, newtext)

    with open(file_absolute_path, 'w') as f:
        f.write(filedata)

def replaceFolderNameOfDjangoFiles(projpath, oldappname, newappname):
    xdirs = [];
    for (dirpath, dirnames, filenames) in os.walk(projpath):
        xdirs.extend(dirnames)
        if(".git" in xdirs): xdirs.remove(".git")
        break
    
    for xdir in xdirs:
        replaceFolderNameOfDjangoFiles(projpath+"/"+xdir,oldappname,newappname)
        if(xdir == oldappname):
            os.rename(projpath+"/"+oldappname,projpath+"/"+newappname)

    # os.rename(projpath+"/"+oldappname,projpath+"/"+newappname)

def nthParent(path,n):
    result = os.sep.join(path.split(os.sep)[:-n])
    return result


initialProjectName  = "django_parliament"
initialApplicationName = "main_app"

newRepoName = sys.argv[1]
newProjectName = sys.argv[2]
newApplicationName = sys.argv[3]

currentfilepath = os.path.dirname(os.path.abspath(__file__))
repopath = nthParent(currentfilepath,3)

replaceTextInDjangoFiles(repopath, initialProjectName ,newProjectName)
replaceTextInDjangoFiles(repopath, initialApplicationName ,newApplicationName)
replaceFolderNameOfDjangoFiles(repopath, initialApplicationName, newApplicationName)
replaceFolderNameOfDjangoFiles(repopath, initialProjectName, newProjectName)

repoparentpath = os.path.abspath(os.path.join(repopath, os.pardir))
os.rename(repopath, repoparentpath+"/"+newRepoName)

