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

    def test_exists(self):
        """There should be a setup.cfg in the project's root directory"""
        assert os.path.exists('setup.cfg')

    def test_description_file(self, setup_cfg):
        """The [metadata] section's description-file should be set to README.rst"""
        assert setup_cfg.has_option('metadata', 'description-file')
        assert setup_cfg.get('metadata', 'description-file') == 'README.rst'
