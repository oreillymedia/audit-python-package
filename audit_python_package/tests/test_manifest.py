# encoding: utf-8
# Created by Jeremy Bowman on Thu Apr 23 10:36:32 EDT 2015
# Copyright (c) 2015 Safari Books Online. All rights reserved.

from __future__ import unicode_literals

import os

import pytest


@pytest.fixture(scope='module')
def manifest():
    """Fixture that provides a list of the entries in MANIFEST.in"""
    if not os.path.exists('MANIFEST.in'):
        return []
    with open('MANIFEST.in', 'rU') as f:
        lines = [line.strip() for line in f.readlines()]
    return lines


class TestManifest(object):
    """Tests related to the MANIFEST.in file"""

    def test_exists(self):
        """There should be a MANIFEST.in file in the project's root directory"""
        assert os.path.exists('MANIFEST.in')

    def test_readme(self, manifest):
        """There should be an entry for README.rst in MANIFEST.in"""
        assert 'include README.rst' in manifest

    def test_requirements(self, manifest):
        """There should be a recursive-include in MANIFEST.in for requirements files"""
        assert 'recursive-include requirements *.txt' in manifest
