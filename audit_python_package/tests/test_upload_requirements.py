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
from subprocess import check_output, STDOUT

import mock

from audit_python_package.command_line import (
    get_branch_name,
    get_repository_name,
    requirements_file_paths,
    update_branch,
    update_repo,
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
    assert len(paths) == 3
    assert 'setup.py' not in paths
    for filename in ['base.txt', 'documentation.txt', 'tests.txt']:
        assert os.path.join('requirements', filename) in paths


def test_update_branch():
    """update_branch() should call requires.io with the expected parameters"""
    repo_name = 'audit-python-package'
    branch_name = 'master'
    paths = ['requirements/base.txt', 'requirements/documentation.txt', 'requirements/tests.txt']
    args = ['requires.io', 'update-branch', '--repository', repo_name,
            '--name', branch_name]
    args.extend(paths)
    with mock.patch('audit_python_package.command_line.check_output') as mock_check_output:
        update_branch(repo_name, branch_name, paths)
        mock_check_output.assert_called_with(args, stderr=STDOUT,
                                             universal_newlines=True)


def test_update_repo():
    """update_repo() should call requires.io with the expected parameters"""
    repo_name = 'audit-python-package'
    args = ['requires.io', 'update-repo', '--repository', repo_name, '--private']
    with mock.patch('audit_python_package.command_line.check_output') as mock_check_output:
        update_repo(repo_name)
        mock_check_output.assert_called_with(args, stderr=STDOUT,
                                             universal_newlines=True)


def test_verify_requires_token_present(monkeypatch):
    """verify_requires_token() should return if the REQUIRES_TOKEN environment variable is set"""
    monkeypatch.setenv('REQUIRES_TOKEN', 'abc123')
    verify_requires_token()


def test_verify_requires_token_not_present(monkeypatch):
    """verify_requires_token() should exit with an error if the REQUIRES_TOKEN environment variable is not set"""
    monkeypatch.delenv('REQUIRES_TOKEN', raising=False)
    with mock.patch('audit_python_package.command_line.sys.exit') as exit_mock:
        verify_requires_token()
        exit_mock.assert_called_with(1)
