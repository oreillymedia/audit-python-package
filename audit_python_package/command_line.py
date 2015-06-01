# encoding: utf-8
# Created by Jeremy Bowman on Thu May 14 10:23:09 EDT 2015
# Copyright (c) 2015 Safari Books Online. All rights reserved.

"""Command line scripts to be installed by setup.py"""

from __future__ import print_function, unicode_literals

import os
import re
from subprocess import CalledProcessError, check_output, STDOUT
import sys

from audit_python_package import get_file_content


def upload_requirements():
    """
    Command line utility to upload requirements files to requires.io.  Can't do
    this easily via tox commands because it doesn't have good support for using
    the output of shell expressions (like one to get the current git branch) as
    command line parameters.  Assumes that a REQUIRES_TOKEN environment
    variable has been set to the requires.io API access token, and that it's
    being run from the project's root directory (the parent of the
    ``requirements`` directory).
    """
    verify_requires_token()
    repository_name = get_repository_name()
    update_repo(repository_name)
    branch_name = get_branch_name()
    paths = requirements_file_paths()
    update_branch(repository_name, branch_name, paths)


def verify_requires_token():
    """Make sure that the REQUIRES_TOKEN environment variable has been set"""
    requires_token = os.getenv('REQUIRES_TOKEN')
    if not requires_token:
        print('REQUIRES_TOKEN environment variable must be set')
        sys.exit(1)


def get_repository_name():
    """Get the name of the repository from setup.py"""
    setup = get_file_content('setup.py')
    match = re.search(r'name=[\'"]([^\'"]+)[\'"]', setup)
    if not match:
        print('Could not find repository name in setup.py')
        sys.exit(1)
    else:
        return match.group(1)


def get_branch_name():
    """Get the name of the current git branch"""
    try:
        return check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], universal_newlines=True).strip()
    except Exception as e:
        print('Error getting current git branch: {}'.format(e))
        print(e.output)
        sys.exit(1)


def requirements_file_paths():
    """List the paths relative to the project root of all requirements files
    that should be uploaded to requires.io.  Excludes
    ``requirements/uninstall.txt``."""
    paths = []
    for filename in os.listdir('requirements'):
        if len(filename) < 5 or filename[-4:] != '.txt' or filename == 'uninstall.txt':
            continue
        path = os.path.join('requirements', filename)
        paths.append(path)
    return paths


def update_repo(repository_name):
    """Create or update a private repository entry in requires.io"""
    try:
        output = check_output(['requires.io', 'update-repo', '--repository', repository_name, '--private'],
                              stderr=STDOUT, universal_newlines=True)
        print(output)
    except CalledProcessError as e:
        print('Unable to create or update {} on requires.io'.format(repository_name))
        print(e.output)
        sys.exit(1)


def update_branch(repository_name, branch_name, paths):
    """Upload the requirements files for the specified git branch to requires.io
    for analysis"""
    args = ['requires.io', 'update-branch', '--repository', repository_name, '--name', branch_name]
    for path in paths:
        args.append(path)
    try:
        output = check_output(args, stderr=STDOUT, universal_newlines=True)
        print(output)
    except CalledProcessError as e:
        print('Unable to update branch {} on requires.io'.format(branch_name))
        print(e.output)
        sys.exit(1)
