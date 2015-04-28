# encoding: utf-8
# Created by Jeremy Bowman on Thu Apr 23 10:36:32 EDT 2015
# Copyright (c) 2015 Safari Books Online. All rights reserved.

from __future__ import unicode_literals

import os

import pytest

from audit_python_package import VERSIONS, get_file_lines


@pytest.fixture(scope='module')
def base():
    """Parsed lines from requirements/base.txt"""
    return get_file_lines(os.path.join('requirements', 'base.txt'))


@pytest.fixture(scope='module')
def documentation():
    """Parsed lines from requirements/documentation.txt"""
    return get_file_lines(os.path.join('requirements', 'documentation.txt'))


@pytest.fixture(scope='module')
def tests():
    """Parsed lines from requirements/tests.txt"""
    return get_file_lines(os.path.join('requirements', 'tests.txt'))


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

    def test_documentation_exists(self):
        """There should be a requirements/documentation.txt file for doc building dependencies"""
        assert os.path.exists(os.path.join('requirements', 'documentation.txt'))

    def test_docutils_version(self, documentation):
        """docutils should be pinned to our currently preferred version"""
        check_version(documentation, 'docutils')

    def test_jinja2_version(self, documentation):
        """Jinja2 should be pinned to our currently preferred version and appear after MarkupSafe"""
        check_version(documentation, 'Jinja2', ['MarkupSafe'])

    def test_markupsafe_version(self, documentation):
        """MarkupSafe should be pinned to our currently preferred version"""
        check_version(documentation, 'MarkupSafe')

    def test_pygments_version(self, documentation):
        """Pygments should be pinned to our currently preferred version"""
        check_version(documentation, 'Pygments')

    def test_sbo_sphinx_version(self, documentation):
        """sbo-sphinx should be pinned to our currently preferred version and appear after Sphinx"""
        check_version(documentation, 'sbo-sphinx', ['Sphinx'])

    def test_sphinx_version(self, documentation):
        """Sphinx should be pinned to our currently preferred version and appear after docutils, Jinja2, and Pygments"""
        check_version(documentation, 'Sphinx', ['docutils', 'Jinja2', 'Pygments'])

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
