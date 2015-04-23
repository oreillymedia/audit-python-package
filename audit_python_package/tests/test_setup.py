# encoding: utf-8
# Created by Jeremy Bowman on Thu Apr 23 10:36:32 EDT 2015
# Copyright (c) 2015 Safari Books Online. All rights reserved.

from __future__ import unicode_literals

import os

import pytest


@pytest.fixture(scope='module')
def setup():
    """Fixture containing the text content of setup.py"""
    if not os.path.exists('setup.py'):
        return ''
    with open('setup.py', 'r') as f:
        content = f.read()
    return content


class TestSetup(object):
    """Checks related to setup.py"""

    def test_exists(self):
        """There should be a setup.py in the project's root directory"""
        assert os.path.exists('setup.py')

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
