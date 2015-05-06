# encoding: utf-8
# Created by Jeremy Bowman on Thu Apr 23 10:36:32 EDT 2015
# Copyright (c) 2015 Safari Books Online. All rights reserved.

from __future__ import unicode_literals

import os
import re

import pytest

from audit_python_package import parse_config_file


@pytest.fixture(scope='module')
def tox_ini():
    """Fixture containing the parsed content of tox.ini"""
    return parse_config_file('tox.ini')


@pytest.fixture(scope='module')
def docs_commands(tox_ini):
    """Fixture containing the commands entry from [testenv:docs]"""
    if not tox_ini.has_option('testenv:docs', 'commands'):
        return []
    return [line.strip() for line in tox_ini.get('testenv:docs', 'commands').split('\n')]


@pytest.fixture(scope='module')
def testenv_commands(tox_ini):
    """Fixture containing the commands entry from [testenv]"""
    if not tox_ini.has_option('testenv', 'commands'):
        return []
    return [line.strip() for line in tox_ini.get('testenv', 'commands').split('\n')]


class TestTox(object):
    """Checks related to tox.ini"""

    def test_tox_ini_exists(self):
        """There should be a tox.ini in the project's root directory"""
        assert os.path.exists('tox.ini')

    def test_tox_section_exists(self, tox_ini):
        """There should be a [tox] section in tox.ini"""
        assert tox_ini.has_section('tox')

    def test_no_downloadcache(self, tox_ini):
        """There should be no downloadcache line in tox.ini (it's deprecated)"""
        assert not tox_ini.has_option('tox', 'downloadcache')

    def test_python_34(self, tox_ini):
        """Python 3.4 should be among the tested configurations"""
        assert tox_ini.has_option('tox', 'envlist')
        assert '34' in tox_ini.get('tox', 'envlist')

    def test_pytest_section_exists(self, tox_ini):
        assert tox_ini.has_section('pytest')

    def test_coverage_modules_specified(self, tox_ini):
        """The pytest section should have an addopts entry which specifies the modules of interest for test coverage"""
        assert tox_ini.has_option('pytest', 'addopts')
        assert re.search(r'--cov \w+', tox_ini.get('pytest', 'addopts'))

    def test_coverage_term_missing(self, tox_ini):
        """The pytest section should have an addopts entry which specifies that the line numbers for missing coverage should be reported"""
        assert tox_ini.has_option('pytest', 'addopts')
        assert '--cov-report term-missing' in tox_ini.get('pytest', 'addopts')

    def test_norecursedirs(self, tox_ini):
        """Directories which shouldn't be searched for tests should be specified"""
        assert tox_ini.has_option('pytest', 'norecursedirs')
        dir_list = tox_ini.get('pytest', 'norecursedirs').split()
        assert '.*' in dir_list
        assert 'docs' in dir_list
        assert 'requirements' in dir_list
        assert 've' in dir_list

    def test_testenv_section_exists(self, tox_ini):
        """There should be a [testenv] section in tox.ini"""
        assert tox_ini.has_section('testenv')

    def test_deps(self, tox_ini):
        """There should be a "deps" line for dependencies under [testenv]"""
        assert tox_ini.has_option('testenv', 'deps')

    def test_testenv_installs_testing_dependencies(self, testenv_commands):
        """There should be a command in testenv to install the testing dependencies from requirements/tests.txt"""
        assert any([re.match(r'pip .*install .*--requirement requirements/tests.txt.*', command) for command in testenv_commands])

    def test_testenv_uses_pytest(self, testenv_commands):
        """pytest should be the default test runner"""
        assert any([command.startswith('py.test') for command in testenv_commands])

    def test_pytest_uses_posargs(self, testenv_commands):
        """The py.test command should accept positional arguments for running specific tests"""
        assert any([re.search(r'py\.test [^\n]*\{posargs', command) for command in testenv_commands])

    def test_docs_section_exists(self, tox_ini):
        """There should be a [testenv:docs] section in tox.ini"""
        assert tox_ini.has_section('testenv:docs')

    def test_docs_check_readme(self, docs_commands):
        """The docs test environment should include a validation of README.rst"""
        assert 'python setup.py check --restructuredtext --strict' in docs_commands

    def test_docs_sphinx_build(self, docs_commands):
        """The docs test environment should include a sphinx-build command"""
        assert 'sphinx-build -b {posargs:html} docs docs/_build' in docs_commands
