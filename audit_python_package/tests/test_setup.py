# encoding: utf-8
# Created by Jeremy Bowman on Thu Apr 23 10:36:32 EDT 2015
# Copyright (c) 2015 Safari Books Online. All rights reserved.

from __future__ import unicode_literals

import os
import re

import pytest

from audit_python_package import get_file_content


@pytest.fixture(scope='module')
def setup():
    """Fixture containing the text content of setup.py"""
    return get_file_content('setup.py')


class TestSetup(object):
    """Checks related to setup.py"""

    def test_exists(self):
        """There should be a setup.py in the project's root directory"""
        assert os.path.exists('setup.py')

    def test_changelog_reminder(self, setup):
        """There should be a reminder in setup.py to update docs/CHANGELOG.rst when the version changes"""
        assert 'docs/CHANGELOG.rst' in setup

    def test_environment_markers(self, setup):
        """If install_requires is derived from a requirements file, it should respect environment markers"""
        if 'parse_requirements' in setup:
            assert '.match_markers()' in setup

    def test_include_package_data(self, setup):
        """include_package_data should be set to True in setup.py (to let MANIFEST.in define the data to include)"""
        assert 'include_package_data=True' in setup

    def test_long_description(self, setup):
        """The package's long_description should be set to the content of README.rst"""
        assert 'import codecs' in setup
        assert "with codecs.open('README.rst', 'r', 'utf-8') as f:" in setup
        assert 'long_description = f.read()' in setup
        assert 'long_description=long_description,' in setup

    def test_no_package_data(self, setup):
        """package_data should not be set in setup.py (use MANIFEST.in instead)"""
        assert not re.search(r'\spackage_data', setup)

    def test_prevent_pypi_upload(self, setup):
        """There should be an invalid "Private :: Do Not Upload" classifier in private packages to prevent accidental uploads to PyPI"""
        assert 'Private :: Do Not Upload' in setup

    def test_read_the_docs(self, setup):
        """There should be explicit support for Read the Docs builds in setup.py"""
        assert 'READTHEDOCS' in setup
        assert 'documentation.txt' in setup

    def test_multiple_pip_versions(self, setup):
        """setup.py should work with a good variety of pip versions"""
        assert 'PipSession()' in setup
        assert ', session=session)' in setup
        assert 'str(r.req)' in setup
        assert '[r.req' not in setup
