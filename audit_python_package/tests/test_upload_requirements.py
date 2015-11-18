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
import re
from subprocess import CalledProcessError, check_output, STDOUT
try:
    from unittest import mock
except ImportError:
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


def test_get_branch_name_error(capsys):
    """get_branch_name() should print useful information and exit if the git command fails"""
    msg = '-bash: git: command not found'

    def side_effect(*args, **kwargs):
        raise CalledProcessError(1, 'cmd', msg)
    with mock.patch('audit_python_package.command_line.check_output') as mock_check_output:
        mock_check_output.side_effect = side_effect
        with mock.patch('audit_python_package.command_line.sys.exit') as mock_exit:
            get_branch_name()
            mock_exit.assert_called_with(1)
    out, err = capsys.readouterr()
    assert 'Error getting current git branch: ' in out
    assert msg in out


def test_get_repository_name():
    """get_repository_name() should return the name of the package from setup.py"""
    assert get_repository_name() == 'audit-python-package'


def test_get_repository_name_error(capsys):
    """get_repository_name() should print useful information and exit if the package name cannot be found in setup.py"""
    with mock.patch('audit_python_package.command_line.get_file_content') as mock_setup:
        mock_setup.return_value = 'Good luck parsing a package name from this'
        with mock.patch('audit_python_package.command_line.sys.exit') as mock_exit:
            get_repository_name()
            mock_exit.assert_called_with(1)
    out, err = capsys.readouterr()
    assert 'Could not find repository name in setup.py' in out


def test_requirements_file_paths():
    """requirements_file_paths() should return the correct set of files to upload to requires.io"""
    paths = requirements_file_paths()
    assert len(paths) == 5
    assert 'setup.py' not in paths
    for filename in ['analyze.txt', 'base.txt', 'documentation.txt', 'tests.txt', 'tox.txt']:
        assert os.path.join('requirements', filename) in paths


def test_python_files_not_uploaded():
    """Files in the requirements directory which aren't *.txt files should not be uploaded"""
    with mock.patch('audit_python_package.command_line.os.listdir') as mock_listdir:
        mock_listdir.return_value = ['base.txt', 'cleanup_requirements.py']
        paths = requirements_file_paths()
        assert paths == [os.path.join('requirements', 'base.txt')]


def test_uninstall_txt_not_uploaded():
    """requirements/uninstall.txt should not be uploaded"""
    with mock.patch('audit_python_package.command_line.os.listdir') as mock_listdir:
        mock_listdir.return_value = ['base.txt', 'uninstall.txt']
        paths = requirements_file_paths()
        assert paths == [os.path.join('requirements', 'base.txt')]


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


def test_update_branch_error(capsys):
    """update_branch() should print useful information and exit if the requires.io command fails"""
    repo_name = 'audit-python-package'
    branch_name = 'master'
    paths = ['requirements/base.txt', 'requirements/documentation.txt', 'requirements/tests.txt']
    msg = 'Something went horribly wrong'

    def side_effect(*args, **kwargs):
        raise CalledProcessError(1, 'cmd', msg)
    with mock.patch('audit_python_package.command_line.check_output') as mock_check_output:
        mock_check_output.side_effect = side_effect
        with mock.patch('audit_python_package.command_line.sys.exit') as mock_exit:
            update_branch(repo_name, branch_name, paths)
            mock_exit.assert_called_with(1)
    out, err = capsys.readouterr()
    assert re.search(r'Unable to update branch .* on requires.io', out)
    assert msg in out


def test_update_repo():
    """update_repo() should call requires.io with the expected parameters"""
    repo_name = 'audit-python-package'
    args = ['requires.io', 'update-repo', '--repository', repo_name, '--private']
    with mock.patch('audit_python_package.command_line.check_output') as mock_check_output:
        update_repo(repo_name)
        mock_check_output.assert_called_with(args, stderr=STDOUT,
                                             universal_newlines=True)


def test_update_repo_error(capsys):
    """update_repo() should print useful information and exit if the requires.io command fails"""
    repo_name = 'audit-python-package'
    msg = 'Insert mysterious network error here'

    def side_effect(*args, **kwargs):
        raise CalledProcessError(1, 'cmd', msg)
    with mock.patch('audit_python_package.command_line.check_output') as mock_check_output:
        mock_check_output.side_effect = side_effect
        with mock.patch('audit_python_package.command_line.sys.exit') as mock_exit:
            update_repo(repo_name)
            mock_exit.assert_called_with(1)
    out, err = capsys.readouterr()
    assert 'Unable to create or update audit-python-package on requires.io' in out
    assert msg in out


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
