# encoding: utf-8
# Created by Jeremy Bowman on Fri Jun  5 11:03:28 EDT 2015
# Copyright (c) 2015 Safari Books Online. All rights reserved.

"""Tests related to the requirements/clean_up_requirements.py script"""

from __future__ import unicode_literals

import os

import pytest

from audit_python_package import get_file_content

SCRIPT_PATH = os.path.join('requirements', 'clean_up_requirements.py')


@pytest.fixture(scope='module')
def clean_up_requirements():
    """Fixture containing the text content of requirements/clean_up_requirements.py"""
    return get_file_content(SCRIPT_PATH)


def test_script_exists():
    """There should be a requirements/clean_up_requirements.py script"""
    assert os.path.exists(SCRIPT_PATH)


def test_only_runs_if_top_level(clean_up_requirements):
    """requirements/clean_up_requirements.py should only do its work if called directly"""
    assert "if __name__ == '__main__':" in clean_up_requirements


def test_uninstalls_previous_dependencies(clean_up_requirements):
    """requirements/clean_up_requirements.py should uninstall any former dependencies"""
    assert "requirements_path = os.path.join(requirements_dir, 'uninstall.txt')" in clean_up_requirements
    assert 'Uninstalling former requirements...' in clean_up_requirements
    assert 'req.uninstall(auto_confirm=True)' in clean_up_requirements


def test_setuptools_installation(clean_up_requirements):
    """requirements/clean_up_requirements.py should install the correct setuptools version"""
    assert "match = re.search(r'^setuptools==([\d\.]+)$', requirements, re.MULTILINE)" in clean_up_requirements
    assert "os.system('pip install setuptools=={}'.format(match.group(1)))" in clean_up_requirements


def test_pip_installation(clean_up_requirements):
    """requirements/clean_up_requirements.py should install the correct pip version"""
    assert "match = re.search(r'^pip==([\d\.]+)$', requirements, re.MULTILINE)" in clean_up_requirements
    assert "os.system('pip install pip=={}'.format(match.group(1)))" in clean_up_requirements
