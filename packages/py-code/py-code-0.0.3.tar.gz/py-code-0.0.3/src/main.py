import os
import shutil
from distutils.dir_util import copy_tree
import sys

from git import Repo
from git import rmtree


def createProjectDirectory(projectName):
    cwd = os.getcwd()
    path = os.path.join(cwd, projectName)
    return path


def copyBoilerplate(templateDirectory, targetDirectory):
    return shutil.copytree(templateDirectory, targetDirectory)


def updateBoilerplate(templateDirectory, targetDirectory):
    return copy_tree(templateDirectory, targetDirectory)


def main():
    #    print("hello world")

    temporaryPath = createProjectDirectory("_temporary")
    os.makedirs(temporaryPath)
    github_url = "https://github.com/sabernetic/py-code"
    Repo.clone_from(github_url, temporaryPath)

    option = " ".join(sys.argv[1:])
    templateDirectory = os.path.join(temporaryPath, "/boilerplate")

    if option == "":
        print("You need to input your action")
    elif option == "update":
        cwd = os.getcwd()
        updateBoilerplate(templateDirectory, cwd)
    else:
        targetDirectory = createProjectDirectory(option)
        copyBoilerplate(templateDirectory, targetDirectory)
    rmtree(temporaryPath)
