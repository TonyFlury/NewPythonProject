#!/usr/bin/env python
# coding=utf-8
"""
# pyORM : Implementation of testing_utils.py

Summary : 
    <summary of migration_class/class being implemented>
Use Case : 
    As a <actor> I want <outcome> So that <justification>

Testable Statements :
    Can I <Boolean statement>
    ....
"""
import sys
import re
import unittest
from copy import copy
from io import StringIO
import logging

import inspect
import click

__version__ = "0.1"
__author__ = 'Tony Flury : anthony.flury@btinternet.com'
__created__ = '13 Sep 2017'


class TestCaeExt:
    def assertRegexSearch(self:unittest.TestCase, text, regex, msg=None):
        msg = msg + '\ntext: {text}\nregex: {regex}\n' if msg else 'regex not found in:\n{text}\n{regex}'
        if not re.search(regex,text):
            raise self.failureException(msg.format(text=text,regex=regex))

    def assertNotRegexSearch(self:unittest.TestCase, text, regex, msg=None):
        msg = msg + '\ntext: {text}\nregex: {regex}\n' if msg else 'regex not found in:\n{text}\n{regex}'
        msg = msg if msg else 'regex found in:\n{text}\n{regex}'
        if re.search(regex,text):
            raise self.failureException(msg.format(text=text,regex=regex))

class Invariant:
    """Context Manager to ensure that object or objects don't change in the scope"""

    def __init__(self, *objs):
        """Conext manager to confirm that an object doesn't change within that context

           Confirms that the each attribute is bound to the same value or to a object which tests equal
           this is a shallow comparison only - it doesn't test attributes of attrributes.
        """
        self._objs = list(objs)
        self._old_objs = [copy(obj) for obj in self._objs]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            return False


        for index, (obj, old_obj) in enumerate(
                zip(self._objs, self._old_objs)):

            if obj is None and old_obj is None:
                continue

            for att in obj.__dict__:
                if getattr(obj, att) is getattr(old_obj, att):
                    continue
                else:
                    raise ValueError(
                        '\'{name}\' attribute is different on object index {index}: \noriginal : {original!r}\n     now : {now!r}'.format(
                            name=att, now=getattr(obj, att),
                            index=index,
                            original=getattr(old_obj, att))) from None


class LogContains:
    """Context Manager to wrap a test execution to test for contents of logs"""
    def __init__(self, logger_name=None, expected='', expected_regex=r''):
        """Conext manager to test for logging content

        Temporarily redirects all logged message into a buffer and tests for the content
        of the buffer when the context manager exits.

        :param logger_name: Optional - the name of the logger instance to test
                        If omitted the root logger is tested
        :param expected: Optional - A string which is expected to be found within the log output
        :param expected_regex: A regex expression which is expected to match at least part of the log output

        if expected parameter and expected_regex are both provided then the expected_regex parameter is ignored.

        By omitting both expected and expected_regex
        """
        self._logger_name = logger_name
        self._expected = expected
        self._expected_regex = expected_regex
        self._handlers = []
        self._logger = None

    def __enter__(self):
        self._buffer = StringIO()
        self._handler = logging.StreamHandler(self._buffer)
        self._logger = logging.getLogger(self._logger_name)
        for handler in self._logger.handlers:
            self._handlers.append(handler)
            self._logger.removeHandler(handler)
        self._level = self._logger.getEffectiveLevel()
        self._logger.addHandler( self._handler)
        self._logger.setLevel(logging.DEBUG)

    def _reset_logger(self):
        self._logger.removeHandler(self._handler)
        for handler in self._handlers:
            self._logger.addHandler(handler)
        self._logger.setLevel(self._level)

    def __exit__(self, exc_type, exc_val, exc_tb):
        exc = None
        self._handler.flush()
        logging_response = self._buffer.getvalue()

        self._reset_logger()

        if exc_type:
            return False

        if self._expected:
            if (self._expected not in logging_response):
                raise ValueError('Expected value not found in logged messages: '+ (logging_response if logging_response else 'Nothing logged')) from None

        if self._expected_regex:
            if (not re.search(self._expected_regex,logging_response)):
                raise ValueError('logged messages doesn\'t match regex: ' + (logging_response if logging_response else 'Nothing logged')) from None

class PatchFunction:
    def __init__(self,module, function, new_callable):
        self._module = sys.modules[module]
        self._function = function
        self._callable = new_callable

    def __enter__(self):
        self._store = getattr(self._module, self._function)
        setattr(self._module, self._function, self._callable)

    def __exit__(self, exc_type, exc_val, exc_tb):
        setattr(self._module, self._function, self._store)
        if exc_type:
            return False


def cli_entry(module):
    """Entry point for all testing modules

      This is called by the testing modules and using closures to set up testing for this module.

      returns the actual entry point to called for this module.
    """

    class OrderedTestSuite(unittest.TestSuite):
        """Order the test suite by the name of the test case - this allows naming to ensure test ordering"""
        def __iter__(self):
            return iter(sorted(self._tests, key=lambda x: str(x)))

    # noinspection PyMissingOrEmptyDocstring,PyUnusedLocal
    def _load_tests(loader, excludes=None, includes=None):
        """"Load tests from all of the relevant classes, and order them"""
        classes = [cls for name, cls in inspect.getmembers(module, inspect.isclass)
                       if issubclass(cls, unittest.TestCase)]

        suite = OrderedTestSuite()
        for test_class in classes:
            tests = loader.loadTestsFromTestCase(test_class)
            if include:
                tests = [test for test in tests if all(re.search(pattern, test.id()) for pattern in include)]
            if excludes:
                tests = [test for test in tests if
                         not any(re.search(exclude_pattern, test.id()) for exclude_pattern in excludes)]
            suite.addTests(tests)
        return suite

    @click.command()
    @click.option('-v', '--verbose', default=2, help='Level of output', count=True)
    @click.option('-s', '--silent', is_flag=True, default=False, help='Supress all output apart from a summary line of dots and test count')
    @click.option('-x', '--exclude', metavar='EXCLUDE', multiple=True, help='Exclude where the names contain the [EXCLUDE] pattern')
    @click.option('-i', '--include', metavar='INCLUDE', multiple=True,
                  help='Include tests where the names contain the [INCLUDE] pattern')
    def _cli_Entry(verbose, silent, exclude, include):
        """Execute the unit test cases where the test id match the patterns

        Test cases are only included for execution if their names (the class name and the method name)
        contain any of the text in any of the [PATTERNS].
        Test cases are excluded from execution if their names contain any of the text in any of the [EXCLUSION]
        patterns

        This is the actual cli_entry point - it is called when the cli is invoked.

        Both [PATTERNS] and [EXCLUSION] can be regular expressions (using the re syntax)

        \b
        A single -v produces a single '.' for each test executed
        Using -v -v produces an output of the method name and 1st line of any
            doc string for each test executed
        """

        verbose = 0 if silent else verbose

        ldr = unittest.TestLoader()
        test_suite = _load_tests(ldr, excludes=exclude, includes = include)
        unittest.TextTestRunner(verbosity=verbose).run(test_suite)

    return _cli_Entry