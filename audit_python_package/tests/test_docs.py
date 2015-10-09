# encoding: utf-8
# Created by Jeremy Bowman on Mon Apr 27 13:55:23 EDT 2015
# Copyright (c) 2015 Safari Books Online. All rights reserved.

from __future__ import unicode_literals

import os

import pytest

from audit_python_package import get_file_content


@pytest.fixture(scope='module')
def conf():
    """Fixture for the text content of docs/conf.py"""
    return get_file_content(os.path.join('docs', 'conf.py'))


@pytest.fixture(scope='module')
def index():
    """Fixture for the text content of docs/index.rst"""
    return get_file_content(os.path.join('docs', 'index.rst'))


class TestDocs(object):
    """
    Tests of the "docs" folder for documentation.  This is the usual location
    of easy-to-edit text documentation files to be converted by Sphinx into
    easier-to-read-and-search documentation in HTML, EPUB, PDF, or other
    formats.  There are other ways to write documentation, but this one is by
    far the most common and well understood in the Python community.

    These tests additionally recommend use of the sbo-sphinx library, which
    simplifies the conf.py module and makes it possible to auto-generate
    Python API documentation from the source code during Read the Docs
    documentation builds (among other benefits).
    """

    def test_conf_exists(self):
        """There should be a docs/conf.py file with basic configuration info for the docs"""
        assert os.path.exists(os.path.join('docs', 'conf.py'))

    def test_sbo_sphinx_imports(self, conf):
        """The default configuration from sbo-sphinx should be imported in docs/conf.py"""
        assert 'from sbo_sphinx.conf import *' in conf

    def test_project_name_specified(self, conf):
        """The "project" variable should be set in docs/conf.py"""
        assert 'project = ' in conf

    def test_apidoc_exclude(self, conf):
        """The "apidoc_exclude" variable should be set in docs/conf.py to a list of modules to exclude from the API documentation"""
        assert 'apidoc_exclude = [' in conf

    def test_index_exists(self):
        """There should be a docs/index.rst file for the documentation main page"""
        assert os.path.exists(os.path.join('docs', 'index.rst'))

    def test_index_has_toctree(self, index):
        """docs/index.rst should include a "toctree" directive"""
        assert '.. toctree::' in index

    def test_api_docs_in_index(self, index):
        """docs/index.rst should include an entry for the Python API documentation"""
        assert '<python/modules>' in index

    def test_general_index_in_index(self, index):
        """docs/index.rst should include an entry for the general index ("genindex")"""
        assert ':ref:`genindex`' in index

    def test_module_index_in_index(self, index):
        """docs/index.rst should include an entry for the module index ("modindex")"""
        assert ':ref:`modindex`' in index

    def test_search_in_index(self, index):
        """docs/index.rst should include an entry for the search page"""
        assert ':ref:`search`' in index

    def test_readme_exists(self):
        """There should be a docs/readme.rst referencing the root directory's README.rst"""
        path = os.path.join('docs', 'readme.rst')
        assert os.path.exists(path)
        with open(path, 'rU') as f:
            assert '.. include:: ../README.rst' in f.read()

    def test_readme_in_index(self, index):
        """There should be an entry in docs/index.rst for docs/readme.rst"""
        assert 'readme' in index

    def test_changelog_exists(self):
        """There should be a docs/CHANGELOG.rst file for the change history"""
        assert os.path.exists(os.path.join('docs', 'CHANGELOG.rst'))

    def test_changelog_in_index(self, index):
        """There should be an entry in docs/index.rst for docs/CHANGELOG.rst"""
        assert 'CHANGELOG' in index
