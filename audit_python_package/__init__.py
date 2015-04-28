from __future__ import unicode_literals

import codecs
from configparser import ConfigParser
import os

DATA_DIRECTORY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))

VERSIONS = {
    'cov-core': '1.15.0',
    'coverage': '3.7.1',
    'docutils': '0.12',
    'Jinja2': '2.7.3',
    'MarkupSafe': '0.23',
    'pip': '6.1.1',
    'py': '1.4.26',
    'Pygments': '2.0.2',
    'pytest': '2.7.0',
    'pytest-catchlog': '1.0',
    'pytest-cov': '1.8.1',
    'setuptools': '15.0',
    'sbo-sphinx': '2.0.3',
    'Sphinx': '1.3.1',
    'tox': '1.9.2',
    'virtualenv': '12.1.1',
}


def parse_config_file(path):
    """Get the parsed content of an INI-style config file (using ConfigParser)"""
    config = ConfigParser()
    if os.path.exists(path):
        config.read(path)
    return config


def get_file_content(path):
    """Get the content of the UTF-8 text file at the specified path.
    Used for pytest fixtures."""
    if not os.path.exists(path):
        return ''
    with codecs.open(path, 'r', 'utf-8') as f:
        return f.read()


def get_file_lines(path):
    """Get a list of the lines in the UTF-8 text file at the specified path.
    Strips leading and trailing whitespace from each line.
    Used for pytest fixtures."""
    if not os.path.exists(path):
        return ''
    with codecs.open(path, 'r', 'utf-8') as f:
        return [line.strip() for line in f.readlines()]
