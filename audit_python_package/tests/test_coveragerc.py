# encoding: utf-8
# Created by Jeremy Bowman on Thu Apr 23 10:36:32 EDT 2015
# Copyright (c) 2015 Safari Books Online. All rights reserved.

from __future__ import unicode_literals

import os

import pytest

from audit_python_package import parse_config_file


@pytest.fixture(scope='module')
def coveragerc():
    """Fixture for the parsed content of .coveragerc"""
    return parse_config_file('.coveragerc')


class TestCoveragerc(object):
    """
    Tests for the .coveragerc coverage module configuration file.  We exclude
    test files from the coverage.py code coverage report because their
    presence makes it hard to scan the report to see the results for the
    actual implementation code, which we care much more about.  For Django
    projects, it's usually a good idea to omit migrations as well.
    """

    def test_exists(self):
        """There should be a .coveragerc file in the root directory"""
        assert os.path.exists('.coveragerc')

    def test_run_section_exists(self, coveragerc):
        """There should be a [run] section in .coveragerc"""
        assert coveragerc.has_section('run')

    def test_tests_excluded_from_coverage(self, coveragerc):
        """Test modules should be excluded from test coverage statistics"""
        assert coveragerc.has_option('run', 'omit')
        # exact format of the entry depends on project layout, usually "*/tests/*"
        assert 'test' in coveragerc.get('run', 'omit')
