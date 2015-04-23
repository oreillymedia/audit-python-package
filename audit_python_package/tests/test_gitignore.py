# encoding: utf-8
# Created by Jeremy Bowman on Thu Apr 23 10:36:32 EDT 2015
# Copyright (c) 2015 Safari Books Online. All rights reserved.

from __future__ import unicode_literals

import os

import pytest

TEMPLATE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', '.gitignore'))


@pytest.fixture(scope='module')
def gitignore():
    """Fixture for the lines in the .gitignore file"""
    if not os.path.exists('.gitignore'):
        return []
    with open('.gitignore', 'rU') as f:
        lines = [line.strip() for line in f.readlines()]
    return lines


class TestGitignore(object):
    """Tests of the .gitignore file for files to ignore when committing code"""

    def test_exists(self):
        """There should be a .gitignore file in the root directory"""
        assert os.path.exists('.gitignore')

    def test_content(self, gitignore):
        """All of the usual entries should be present in .gitignore"""
        with open(TEMPLATE_PATH, 'rU') as f:
            lines = [line.strip() for line in f.readlines()]
        for line in lines:
            assert line in gitignore
