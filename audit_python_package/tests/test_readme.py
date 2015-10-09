# encoding: utf-8
# Created by Jeremy Bowman on Thu Apr 23 10:36:32 EDT 2015
# Copyright (c) 2015 Safari Books Online. All rights reserved.

from __future__ import unicode_literals

import os


class TestReadme(object):
    """
    Tests of the main README.rst file.  This file is included in Sphinx
    documentation builds, appears on the repository's main page in GitHub, and
    serves as the long description of the package when uploaded to PyPI.
    """

    def test_exists(self):
        """There should be a README.rst in the root directory"""
        assert os.path.exists('README.rst')
