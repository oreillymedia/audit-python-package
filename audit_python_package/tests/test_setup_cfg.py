# encoding: utf-8
# Created by Jeremy Bowman on Thu Apr 23 10:36:32 EDT 2015
# Copyright (c) 2015 Safari Books Online. All rights reserved.

from __future__ import unicode_literals

from configparser import ConfigParser
import os

import pytest


@pytest.fixture(scope='module')
def setup_cfg():
    """Fixture containing the parsed content of setup.cfg"""
    config = ConfigParser()
    if os.path.exists('setup.cfg'):
        config.read('setup.cfg')
    return config


class TestSetupCfg(object):
    """Checks related to setup.cfg"""

    def test_exists(self):
        """There should be a setup.cfg in the project's root directory"""
        assert os.path.exists('setup.cfg')

    def test_description_file(self, setup_cfg):
        """The [metadata] section's description-file should be set to README.rst"""
        assert setup_cfg.has_option('metadata', 'description-file')
        assert setup_cfg.get('metadata', 'description-file') == 'README.rst'
