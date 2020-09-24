#!/usr/bin/env python
# coding=utf-8
"""
# {{cookiecutter.project_repo}} : {{cookiecutter.project_desc}}

Summary :
    {{cookiecutter.project_summary}}
Use Case :
    {{cookiecutter.project_usecase}}

Testable Statements :
    ...
"""
import inspect
import re
import unittest
import re
import click
import sys

from testing_utils import cli_entry

from {{cookiecutter.project_repo}} import {{cookiecutter.project_repo}}


class TestCases(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_000_something(self):
        pass


if __name__ == '__main__':
    cli_entry(sys.modules[__name__])()