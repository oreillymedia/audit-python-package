# encoding: utf-8
# Created by Jeremy Bowman on Thu Apr 23 10:36:32 EDT 2015
# Copyright (c) 2015 Safari Books Online. All rights reserved.

from __future__ import unicode_literals

import os

import pytest

from audit_python_package import parse_config_file


@pytest.fixture(scope='module')
def setup_cfg():
    """Fixture containing the parsed content of setup.cfg"""
    return parse_config_file('setup.cfg')


class TestSetupCfg(object):
    """Checks related to setup.cfg"""

    def test_does_not_exist(self):
        """There should not be a setup.cfg in the project's root directory"""
        # We used to use this to set the package's long description, but now
        # prefer to set long_description in setup.py to the README.rst file
        # content directly; most validation tools only work this way
        assert not os.path.exists('setup.cfg')
