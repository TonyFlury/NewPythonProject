#!/usr/bin/env python
# coding=utf-8
"""
# pyORM : Implementation of test_all.py

Summary : 
    <summary of migration_class/class being implemented>
Use Case : 
    As a <actor> I want <outcome> So that <justification>

Testable Statements :
    Can I <Boolean statement>
    ....
    
Test Series : 

"""

import click
import unittest
import importlib
from pathlib import Path
from os import listdir
import inspect
import re
from testing_utils import OrderedTestSuite

#ToDO - lots of repeated code (or similar code) between this and testing_utils.

# noinspection PyMissingOrEmptyDocstring,PyUnusedLocal
def load_tests(loader, load_module, tests=None, include=None,excludes=None):
    """Load tests from all of the relevant classes, and order them"""
    classes = [cls for name, cls in inspect.getmembers(load_module,
                                                 inspect.isclass)
                                    if issubclass(cls, unittest.TestCase)]
    suite = OrderedTestSuite()
    for test_class in classes:
        tests = loader.loadTestsFromTestCase(test_class)
        if include:
            tests = [test for test in tests if all(re.search(pattern, test.id()) for pattern in include)]
        if excludes:
            tests = [test for test in tests if not any(re.search(exclude_pattern,test.id()) for exclude_pattern in excludes)]
        suite.addTests(tests)
    return suite



@click.command()
@click.option('-v', '--verbose', default=2, help='Level of output', count=True)
@click.option('-s', '--silent', is_flag=True, default=False, help='Supress all output apart from a summary line of dots and test count')
@click.option('-x', '--exclude', metavar='EXCLUDE', multiple=True, help='Exclude test where the names contain the [EXCLUDE] pattern')
@click.option('-i', '--include', metavar='INCLUDE', multiple=True, help='Include tests where the names contain the [INCLUDE] pattern')
@click.option('-m', '--include_modules', metavar='MODULE INCLUDE', multiple=True, required=False, type=str, help='Match modules to include')
@click.option('-e', '--exclude_modules', metavar='MODULE EXCLUDE', multiple=True, required=False, type=str, help='Match modules to exclude')
def main(verbose, silent, include, exclude, include_modules, exclude_modules):
    """Execute all the test cases in all modules in this directory.

    Test cases are only included for execution if their migration_class name matches one of the [MODULE INCLUDE] and their test names (the class name and the method name)
    contain the text in any of the [INCLUDE] patterns.
    Test cases are excluded from execution if their migration_class name contains any of the text in the [MODULE EXCLUDE] patterns or the test names contain any of the text in any of the [EXCLUDE] patterns
    patterns

    [MODULE INCLUDE], [MODULE EXCLUDE], [INCLUDE] and [EXCLUDE] can be regular expressions (using the re syntax)

    \b
    A single -v produces a single '.' for each test executed
    Using -v -v produces an output of the method name and 1st line of any
            doc string for each test executed
    """
    verbose = 0 if silent else verbose

    ldr = unittest.TestLoader()
    suite = OrderedTestSuite()

    this_dir = Path(__file__).parent

    module_names = [py[:-3] for py in listdir(str(this_dir)) if py.endswith('.py') and py.startswith('test_') and py not in ['__init__.py', str(Path(__file__).name )]]

    if include_modules:
        module_names = [name for name in module_names if
                 all(re.search(pattern, name) for pattern in include_modules)]
    if exclude_modules:
        module_names = [name for name in module_names if not any(
            re.search(exclude_pattern, name) for exclude_pattern in
            exclude_modules)]

    for module_name in module_names:
        the_module = importlib.import_module(module_name)
        suite.addTests(load_tests(loader=ldr, load_module=the_module,include=include, excludes=exclude))

    unittest.TextTestRunner(verbosity=verbose).run(suite)

if __name__ == '__main__':
    main()
else:
    import sys
    print('Run test_all direct from the command line - do not run as if it is a unittest moudle')
    sys.exit(1)