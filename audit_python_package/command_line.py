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
    requires_token = os.getenv('REQUIRES_TOKEN')
    if not requires_token:
        print('REQUIRES_TOKEN environment variable must be set')
        sys.exit(1)
    setup = get_file_content('setup.py')
    match = re.search(r'name=[\'"]([^\'"]+)[\'"]', setup)
    if not match:
        print('Could not find repository name in setup.py')
        sys.exit(1)
    repository_name = match.group(1)
    try:
        branch_name = check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], universal_newlines=True).strip()
    except Exception as e:
        print('Error getting current git branch: {}'.format(e))
        sys.exit(1)
    paths = ['setup.py']
    for filename in os.listdir('requirements'):
        if len(filename) < 5 or filename[-4:] != '.txt' or filename == 'uninstall.txt':
            continue
        path = os.path.join('requirements', filename)
        paths.append(path)
    try:
        output = check_output(['requires.io', 'update-repo', '--repository', repository_name, '--private'],
                              stderr=STDOUT, universal_newlines=True)
        print(output)
    except CalledProcessError as e:
        print('Unable to create or update {} on requires.io'.format(repository_name))
        print(e.output)
        sys.exit(1)
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
