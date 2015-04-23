# encoding: utf-8
# Created by Jeremy Bowman on Thu Apr 23 10:36:32 EDT 2015
# Copyright (c) 2015 Safari Books Online. All rights reserved.

from __future__ import unicode_literals

import os

import pytest

from audit_python_package import VERSIONS


def requirements_file_lines(path):
    """Get a list of the lines from the requirements file at the specified path"""
    if not os.path.exists(path):
        return []
    with open(path, 'rU') as f:
        lines = [line.strip() for line in f.readlines()]
    return lines


@pytest.fixture(scope='module')
def base():
    """Parsed lines from requirements/base.txt"""
    path = os.path.join('requirements', 'base.txt')
    return requirements_file_lines(path)


@pytest.fixture(scope='module')
def tests():
    """Parsed lines from requirements/tests.txt"""
    path = os.path.join('requirements', 'tests.txt')
    return requirements_file_lines(path)


def check_version(requirements, package_name, dependencies_list=None):
    """Verify that the named package is pinned at the desired version and appears after its dependencies"""
    entry = '{}=={}'.format(package_name, VERSIONS[package_name])
    assert entry in requirements
    if dependencies_list:
        index = requirements.index(entry)
        for dependency in dependencies_list:
            assert any([entry.startswith('{}=='.format(dependency)) for entry in requirements[:index]])


class TestRequirements(object):
    """Tests involving requirements files"""

    def test_base_exists(self):
        """There should be a requirements/base.txt file for core dependencies"""
        assert os.path.exists(os.path.join('requirements', 'base.txt'))

    def test_setuptools_version(self, base):
        """setuptools should be pinned to our currently preferred version"""
        check_version(base, 'setuptools')

    def test_pip_version(self, base):
        """pip should be pinned to our currently preferred version"""
        check_version(base, 'pip')

    def test_tests_exists(self):
        """There should be a requirements/tests.txt file for testing dependencies"""
        assert os.path.exists(os.path.join('requirements', 'tests.txt'))

    def test_py_version(self, tests):
        """py should be pinned to our currently preferred version"""
        check_version(tests, 'py')

    def test_pytest_version(self, tests):
        """pytest should be pinned to our currently preferred version and appear after py"""
        check_version(tests, 'pytest', ['py'])

    def test_coverage_version(self, tests):
        """coverage should be pinned to our currently preferred version"""
        check_version(tests, 'coverage')

    def test_cov_core_version(self, tests):
        """cov-core should be pinned to our currently preferred version and appear after coverage"""
        check_version(tests, 'cov-core', ['coverage'])

    def test_pytest_cov_version(self, tests):
        """pytest-cov should be pinned to our currently preferred version and appear after cov-core and pytest"""
        check_version(tests, 'pytest-cov', ['pytest', 'cov-core'])

    def test_pytest_catchlog_version(self, tests):
        """pytest-catchlog should be pinned to our currently preferred version and appear after pytest"""
        check_version(tests, 'pytest-catchlog', ['pytest'])

    def test_tox_version(self, tests):
        """tox should be pinned to our currently preferred version and appear after py and virtualenv"""
        check_version(tests, 'tox', ['py', 'virtualenv'])

    def test_virtualenv_version(self, tests):
        """virtualenv should be pinned to our currently preferred version"""
        check_version(tests, 'virtualenv')
