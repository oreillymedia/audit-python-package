# encoding: utf-8
# Created by Jeremy Bowman on Thu Apr 23 10:36:32 EDT 2015
# Copyright (c) 2015 Safari Books Online. All rights reserved.

from __future__ import unicode_literals

import os

import pytest

from audit_python_package import VERSIONS, get_file_lines, get_requirement_lines


@pytest.fixture(scope='module')
def base():
    """Parsed lines from requirements/base.txt"""
    return get_requirement_lines(os.path.join('requirements', 'base.txt'))


@pytest.fixture(scope='module')
def documentation():
    """Parsed lines from requirements/documentation.txt"""
    path = os.path.join('requirements', 'documentation.txt')
    if not os.path.exists(path):
        # Don't punish sbo-sphinx too much for having doc dependencies in base.txt
        path = os.path.join('requirements', 'base.txt')
    return get_requirement_lines(path)


@pytest.fixture(scope='module')
def tests():
    """Parsed lines from requirements/tests.txt"""
    return get_requirement_lines(os.path.join('requirements', 'tests.txt'))


@pytest.fixture(scope='module')
def uninstall():
    """Parsed lines from requirements/uninstall.txt"""
    return get_file_lines(os.path.join('requirements', 'uninstall.txt'))


def check_version(requirements, package_name, dependencies_set=None):
    """Verify that the named package is pinned at the desired version and appears after its dependencies"""
    requirement = '{}=={}'.format(package_name, VERSIONS[package_name])
    assert requirement in requirements
    if dependencies_set:
        index = requirements.index(requirement)
        for dependency in dependencies_set:
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

    def test_other_base_requirement_versions(self, base):
        """All other dependencies declared in base.txt should match any versions we're explicitly trying to standardize on"""
        for line in base:
            package_name, version = (part.strip() for part in line.split('=='))
            if package_name in {'pip', 'setuptools'}:
                continue
            if package_name in VERSIONS:
                assert version == VERSIONS[package_name]

    def test_documentation_exists(self):
        """There should be a requirements/documentation.txt file for doc building dependencies"""
        assert os.path.exists(os.path.join('requirements', 'documentation.txt'))

    def test_alabaster_version(self, documentation):
        """alabaster should be pinned to our currently preferred version and appear after Sphinx"""
        check_version(documentation, 'alabaster', {'Sphinx'})

    def test_babel_version(self, documentation):
        """Babel should be pinned to our currently preferred version and appear after pytz"""
        check_version(documentation, 'Babel', {'pytz'})

    def test_bleach_version(self, documentation):
        """bleach should be pinned to our currently preferred version and appear after html5lib and six"""
        check_version(documentation, 'bleach', {'html5lib', 'six'})

    def test_docutils_version(self, documentation):
        """docutils should be pinned to our currently preferred version"""
        check_version(documentation, 'docutils')

    def test_html5lib_version(self, documentation):
        """html5lib should be pinned to our currently preferred version and appear after six"""
        check_version(documentation, 'html5lib', {'six'})

    def test_jinja2_version(self, documentation):
        """Jinja2 should be pinned to our currently preferred version and appear after MarkupSafe"""
        check_version(documentation, 'Jinja2', {'MarkupSafe'})

    def test_markupsafe_version(self, documentation):
        """MarkupSafe should be pinned to our currently preferred version"""
        check_version(documentation, 'MarkupSafe')

    def test_pygments_version(self, documentation):
        """Pygments should be pinned to our currently preferred version"""
        check_version(documentation, 'Pygments')

    def test_pystemmer_version(self, documentation):
        """PyStemmer should be pinned to our currently preferred version"""
        check_version(documentation, 'PyStemmer')

    def test_pytz_version(self, documentation):
        """pytz should be pinned to our currently preferred version"""
        check_version(documentation, 'pytz')

    def test_readme_version(self, documentation):
        """readme should be pinned to our currently preferred version and appear after bleach, docutils, Pygments, and six"""
        check_version(documentation, 'readme', {'bleach', 'docutils', 'Pygments', 'six'})

    def test_sbo_sphinx_version(self, documentation):
        """sbo-sphinx should be pinned to our currently preferred version and appear after Sphinx"""
        check_version(documentation, 'sbo-sphinx', {'Sphinx'})

    def test_six_version(self, documentation):
        """six should be pinned to our currently preferred version"""
        check_version(documentation, 'six')

    def test_snowballstemmer(self, documentation):
        """snowballstemmer should be pinned to our currently preferred version"""
        check_version(documentation, 'snowballstemmer')

    def test_sphinx_rtd_theme(self, documentation):
        """sphinx_rtd_theme should be pinned to our currently preferred version and appear after Sphinx"""
        check_version(documentation, 'sphinx_rtd_theme', {'Sphinx'})

    def test_sphinx_version(self, documentation):
        """Sphinx should be pinned to our currently preferred version and appear after Babel, docutils, Jinja2, Pygments, six, and snowballstemmer"""
        check_version(documentation, 'Sphinx', {'Babel', 'docutils', 'Jinja2', 'Pygments', 'six', 'snowballstemmer'})

    def test_tests_exists(self):
        """There should be a requirements/tests.txt file for testing dependencies"""
        assert os.path.exists(os.path.join('requirements', 'tests.txt'))

    def test_gnureadline_version(self, tests):
        """gnureadline should be pinned to our currently preferred version"""
        check_version(tests, 'gnureadline')

    def test_ipdb_version(self, tests):
        """ipdb should be pinned to our currently preferred version and appear after ipython"""
        check_version(tests, 'ipdb', {'ipython'})

    def test_ipython_version(self, tests):
        """ipython should be pinned to our currently preferred version and appear after gnureadline"""
        check_version(tests, 'ipython', {'gnureadline'})

    def test_py_version(self, tests):
        """py should be pinned to our currently preferred version"""
        check_version(tests, 'py')

    def test_pluggy_version(self, tests):
        """pluggy should be pinned to our currently preferred version"""
        check_version(tests, 'pluggy')

    def test_pytest_version(self, tests):
        """pytest should be pinned to our currently preferred version and appear after py"""
        check_version(tests, 'pytest', {'py'})

    def test_coverage_version(self, tests):
        """coverage should be pinned to our currently preferred version"""
        check_version(tests, 'coverage')

    def test_cov_core_version(self, tests):
        """cov-core should be pinned to our currently preferred version and appear after coverage"""
        check_version(tests, 'cov-core', {'coverage'})

    def test_pytest_cov_version(self, tests):
        """pytest-cov should be pinned to our currently preferred version and appear after cov-core and pytest"""
        check_version(tests, 'pytest-cov', {'pytest', 'cov-core'})

    def test_pytest_catchlog_version(self, tests):
        """pytest-catchlog should be pinned to our currently preferred version and appear after pytest"""
        check_version(tests, 'pytest-catchlog', {'pytest'})

    def test_tox_version(self, tests):
        """tox should be pinned to our currently preferred version and appear after pluggy, py, and virtualenv"""
        check_version(tests, 'tox', {'pluggy', 'py', 'virtualenv'})

    def test_virtualenv_version(self, tests):
        """virtualenv should be pinned to our currently preferred version"""
        check_version(tests, 'virtualenv')

    def test_uninstall_exists(self):
        """There should be a requirements/uninstall.txt file for listing previous dependencies to uninstall"""
        assert os.path.exists(os.path.join('requirements', 'uninstall.txt'))

    def test_uninstall_explanation(self, uninstall):
        """requirements/uninstall.txt should include a comment explaining its usage"""
        assert uninstall[0] == '# Packages which were once dependencies, but should now be removed if present.'

    def test_cpython2_does_not_exist(self):
        """There should not be a requirements/cpython2.txt file, use environment markers instead"""
        assert not os.path.exists(os.path.join('requirements', 'cpython2.txt'))

    def test_cpython3_does_not_exist(self):
        """There should not be a requirements/cpython3.txt file, use environment markers instead"""
        assert not os.path.exists(os.path.join('requirements', 'cpython3.txt'))

    def test_pypy_does_not_exist(self):
        """There should not be a requirements/pypy.txt file, use environment markers instead"""
        assert not os.path.exists(os.path.join('requirements', 'pypy.txt'))
