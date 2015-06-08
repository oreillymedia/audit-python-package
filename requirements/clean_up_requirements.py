#!/usr/bin/env python
# encoding: utf-8
# Created by Jeremy Bowman on Wed May 13 14:36:58 EDT 2015
# Copyright (c) 2015 Safari Books Online, LLC. All rights reserved.

"""
Utility to uninstall any installed packages listed in uninstall.txt.  Can't use
``pip uninstall -r`` because it aborts after the first package in the list
which isn't currently installed.  Also installs the currently-recommended
versions of setuptools and pip from requirements/nest.txt (to avoid needing
to replicate this logic in git-hooks/post-merge, tox.ini, quilter, etc.)
"""

from __future__ import print_function, unicode_literals

import codecs
import os
import re

from pip.download import PipSession
from pip.exceptions import UninstallationError
from pip.index import PackageFinder
from pip.req import parse_requirements


if __name__ == '__main__':
    requirements_dir = os.path.abspath(os.path.dirname(__file__))
    requirements_path = os.path.join(requirements_dir, 'uninstall.txt')

    session = PipSession()
    finder = PackageFinder([], [], session=session)
    requirements = parse_requirements(requirements_path, finder, session=session)
    print('Uninstalling former requirements...')
    for req in requirements:
        try:
            req.uninstall(auto_confirm=True)
            print('Uninstalled {}'.format(req.name))
        except UninstallationError as e:
            if 'not installed' in e.message:
                # Good, the whole point was that we don't want it installed
                pass
            else:
                # We probably want to hear about any other uninstallation problems
                raise
    print('Done')

    # Install the currently recommended setuptools and pip versions
    with codecs.open('requirements/base.txt', 'r', 'utf-8') as f:
        requirements = f.read()
    match = re.search(r'^setuptools==([\d\.]+)$', requirements, re.MULTILINE)
    os.system('pip install setuptools=={}'.format(match.group(1)))
    match = re.search(r'^pip==([\d\.]+)$', requirements, re.MULTILINE)
    os.system('pip install pip=={}'.format(match.group(1)))
