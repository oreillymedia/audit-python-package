# encoding: utf-8
# Created by Jeremy Bowman on Mon Apr 27 13:55:23 EDT 2015
# Copyright (c) 2015 Safari Books Online. All rights reserved.

from __future__ import unicode_literals

import os
import re

import pytest

from audit_python_package import DATA_DIRECTORY_PATH, get_file_content, VERSIONS


@pytest.fixture(scope='module')
def install_hooks():
    """Fixture for the text content of git-hooks/install-hooks"""
    return get_file_content(os.path.join('git-hooks', 'install-hooks'))


@pytest.fixture(scope='module')
def post_merge():
    """Fixture for the text content of git-hooks/post-merge"""
    return get_file_content(os.path.join('git-hooks', 'post-merge'))


class TestGitHooks(object):
    """Tests for git hooks to update the local virtualenv after each git
    pull/checkout/merge.  This may become obsolete after transitioning to
    running most code in Docker containers in a Vagrant VM, but for now it's
    still useful to have these hooks."""

    def test_install_hooks_exists(self):
        """There should be an executable git-hooks/install-hooks script"""
        assert os.access(os.path.join('git-hooks', 'install-hooks'), os.X_OK)

    def test_install_hooks_content(self, install_hooks):
        """git-hooks/install-hooks should be a Python 2/3-compatible script for installing the post-merge script"""
        assert install_hooks.startswith('#!/usr/bin/env python')
        script = get_file_content(os.path.join(DATA_DIRECTORY_PATH, 'install-hooks'))
        assert script in install_hooks

    def test_post_merge_exists(self):
        """There should be an executable git-hooks/post-merge script"""
        assert os.access(os.path.join('git-hooks', 'post-merge'), os.X_OK)

    def test_post_merge_uses_python(self, post_merge):
        """git-hooks/post-merge should be a directly executable Python script"""
        assert post_merge.startswith('#!/usr/bin/env python')

    def test_post_merge_pyton_3_compatible(self, post_merge):
        """git-hooks/post-merge should work with either Python 2 or 3"""
        assert 'print_function' in post_merge
        assert 'unicode_literals' in post_merge
        assert 'universal_newlines=True' in post_merge
        assert 'print ' not in post_merge

    def test_post_merge_deletes_pyc_files(self, post_merge):
        """git-hooks/post-merge should delete any *.pyc files under the root directory"""
        assert 'os.system("find . -name \'*pyc\' -delete")' in post_merge

    def test_post_merge_setuptools(self, post_merge):
        """git-hooks/post-merge should install the correct version of setuptools"""
        assert 'os.system("pip install setuptools=={}")'.format(VERSIONS['setuptools']) in post_merge

    def test_post_merge_pip(self, post_merge):
        """git-hooks/post-merge should install the correct version of pip"""
        assert 'os.system("pip install pip=={}")'.format(VERSIONS['pip']) in post_merge

    def test_post_merge_test_dependencies(self, post_merge):
        """git-hooks/post-merge should install the additional dependencies needed to run tests"""
        assert re.search(r'pip install [^"\']*--requirement requirements/tests.txt', post_merge)

    def test_post_merge_installs_package(self, post_merge):
        """git-hooks/post-merge should install the package contained in the git repository"""
        assert re.search(r'pip install [^"\']*--editable ./', post_merge)
