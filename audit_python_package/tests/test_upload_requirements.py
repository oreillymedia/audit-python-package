# encoding: utf-8
# Created by Jeremy Bowman on Thu Apr 23 10:36:32 EDT 2015
# Copyright (c) 2015 Safari Books Online. All rights reserved.

"""
Tests of the upload_requirements script for requires.io integration.
Unlike most other tests in this package, this one is not packaged for use in
other repositories.
"""

from __future__ import unicode_literals

import os
from subprocess import check_output

import mock

from audit_python_package.command_line import (
    get_branch_name,
    get_repository_name,
    requirements_file_paths,
    verify_requires_token
)


def test_get_branch_name():
    """get_branch_name() should return a valid git branch name"""
    check_output(['git', 'check-ref-format', '--branch', get_branch_name()])


def test_get_repository_name():
    """get_repository_name() should return the name of the package from setup.py"""
    assert get_repository_name() == 'audit-python-package'


def test_requirements_file_paths():
    """requirements_file_paths() should return the correct set of files to upload to requires.io"""
    paths = requirements_file_paths()
    assert len(paths) == 4
    assert 'setup.py' in paths
    for filename in ['base.txt', 'documentation.txt', 'tests.txt']:
        assert os.path.join('requirements', filename) in paths


def test_verify_requires_token_present(monkeypatch):
    """verify_requires_token() should return if the REQUIRES_TOKEN environment variable is set"""
    monkeypatch.setenv('REQUIRES_TOKEN', 'abc123')
    verify_requires_token()


def test_verify_requires_token_not_present(monkeypatch):
    """verify_requires_token() should exit with an error if the REQUIRES_TOKEN environment variable is set"""
    monkeypatch.delenv('REQUIRES_TOKEN', raising=False)
    with mock.patch('audit_python_package.command_line.sys.exit') as exit_mock:
        verify_requires_token()
        exit_mock.assert_called_with(1)
