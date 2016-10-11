========================================
New Python Project cookiecutter template
========================================

This cookie cutter template is designed primarily for my personal
use but it does contain a number of features which may well be
interesting to other people : 

#. Automated creation of github repository
#. Options for Py27 and Py35 projects
#. Automated creation of virtual environments for Py27 & Py35
#. Special case for cli projects (adds click module to virtual enviornments - can be extended)
#. Initial config for Sphinx documentation tool, and initial documentationsource code
#. Special case for creation of project without github rep creation
#. Initial config for tox & travis
#. Options for choice of license (MIT, GNU, Apache - easily extensible)
#. Initial config for PyCharm - including recording virtual envs and opening first source code and README file
    
If you find any issues - please let me know.

Usage
-----

Direct Use from github
######################

To use this template directly (without further customisation) : 

.. code-block:: bash

    $ cookiecutter gh:TonyFlury/NewPythonProject

Customise before use
####################

To customise this template before use : 

.. code-block:: bash

    $ cd Development
    $ git clone git@github.com:TonyFlury/NewPythonProject.git
 
Modify the variables defined in cookiecutter.json.

Open up the skeleton project. If you need to change it around a bit, do so.

You probably also want to create a repo, name it differently, and push it
as your own new Cookiecutter project template, for handy future use.

Once you have completed your changes - you will generate your new project
from the template

    $ cookiecutter NewPythonProject 
