#!/usr/bin/env python

"""
Cookie Cutter post generation hook

Initialise git
   Add source code files into git

Create Virtualenv
"""
from __future__ import print_function

import os, sys, shutil
import subprocess

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)
TEST_REQ_PATH = os.path.join(PROJECT_DIRECTORY,"test_requirements.txt")
REQ_PATH = os.path.join(PROJECT_DIRECTORY,"requirements.txt")
LICENSE_PATH = os.path.join(PROJECT_DIRECTORY,"LICENSE.rst")

def apply_license():
    """ Rename appropriate license file, and delete un needed files"""

    license_files={"MIT":"MIT License", "GNU GPL v3.0":"GNU GPL v3.0 License", "Apache Software License 2.0":"Apache Software License 2.0"}

    print("\n-------------------------------------")
    print("Apply chosen license")
    
    for li_name, li_file in license_files.iteritems():
        if li_name == "{{cookiecutter.license}}":
            os.rename(os.path.join(PROJECT_DIRECTORY,li_file), 
                      LICENSE_PATH )
        else:
            os.remove(os.path.join(PROJECT_DIRECTORY,li_file))
    shutil.copy(LICENSE_PATH, 
                    os.path.join(PROJECT_DIRECTORY,"docs","LICENSE.rst") )

def apply_git():
    """Apply the relevant files to git, and create github as required"""

    # Initialise and add files to the git repository
    print("\n--------------------------------------")
    print("Initialising git & github remote repo - {{cookiecutter.project_repo}}")
    os.system( "git init .")
    os.system( "git add {{cookiecutter.project_repo}}/*.py" )
    os.system( "git add tests/*.py" )
    os.system( "git add docs/*.rst" )
    os.system( "git add README.rst" )
    os.system( "git add CONTRIBUTING.rst" )
    os.system( "git add setup.py" )
    os.system( "git add tox.ini")
    os.system( "git add .gitignore")
    os.system( "git add .travis.yml")
    os.system( "git add LICENSE.rst")
    os.system( "git add requirements.txt")
    os.system( "git add test_requirements.txt")

    # Perform initial commit project files
    print("\n--------------")
    print("Initial commit")
    os.system( "git commit -m 'Initial commit with cookiecutter create' >/dev/null")

    # create github repository and link local repository
    if "{{cookiecutter.create_external_resources}}" == "Yes":
        print("\n---------------------------")
        print( "Creating remote repository")
        os.system( "git remote add origin {{cookiecutter.project_ghurl}} >/dev/null")
        os.system( "curl -u '{{cookiecutter.author_username}}' https://api.github.com/user/repos -d '{\"name\":\"{{cookiecutter.project_repo}}\",\"description\":\"{{cookiecutter.project_desc}}\"}' >/dev/null")
        os.system( "git push -u origin master" )
    else:
        print( "Warning : Remote Repository NOT created - as per request")


def apply_requirements():
    """Add any additional requirements to the various requirements.txt file"""
    with open(os.path.join(PROJECT_DIRECTORY,"test_requirements.txt"),"a") as test_req, open(os.path.join(PROJECT_DIRECTORY,"requirements.txt"),"a") as req:

        # Add click library for cli based applications
        if "{{cookiecutter.cli}}" == "Yes":
            req.write("click>=6.6\n")
            test_req.write("click>=6.6\n")

        # Add six if Py27 and Py35 are both required
        if "{{cookiecutter.Py27}}" == "Yes" and "{{cookiecutter.Py35}}" == "Yes":
            req.write("six>=1.10\n")
            test_req.write("six>=1.10\n")

def apply_virtualenv():
    print("\n-----------------------")
    print("Initialising virtualenv")
    if "{{cookiecutter.Py27}}" == "Yes":
        print("Creating Python 2.7 environment")
        subprocess.call(['/bin/bash', '-i', '-c', "mkvirtualenv -r '{test_req}' -p /usr/bin/python2.7 {{cookiecutter.project_repo}}27".format(test_req=TEST_REQ_PATH)],
             stdout=sys.stdout,
             stderr=subprocess.STDOUT)

    if "{{cookiecutter.Py35}}" == "Yes":
        print("Creating Python 3.5 environment")
        subprocess.call(['/bin/bash', '-i', '-c', "mkvirtualenv -r '{test_req}' -p /usr/bin/python3.5 {{cookiecutter.project_repo}}35".format(test_req=TEST_REQ_PATH)],
             stdout=sys.stdout,
             stderr=subprocess.STDOUT)


def add_bug_reporting():
    """Add the Bug reporting section to the README.rst"""
    section = """
Every care is taken to try to ensure that this code comes to you bug free.
If you do find an error - please report the problem on :
`GitHub <{{cookiecutter.project_gh}}>`_
or
by email to : `{{cookiecutter.author}} <mailto:{{cookiecutter.author_email}}?Subject={{cookiecutter.project_repo}}%20Error>`_
""".split("\n")

    max_len = max(map(len,section))
    max_len = max_len + (max_len % 2)

    with open(os.path.join(PROJECT_DIRECTORY,"README.rst"), "a") as readme:
        readme.write("+" + "-"*max_len + "+\n")
        readme.write("|" + " "*(max_len/2-2) + "Bugs" + " "*(max_len/2-2) + "+\n")
        readme.write("+" + "="*max_len + "+\n")
        for l in section:
            readme.write("|" + l + " "*(max_len-len(l)) + "|\n")
        readme.write("+" + "-"*max_len + "+\n")

apply_license()

add_bug_reporting()

apply_requirements()

apply_git()

apply_virtualenv()


