from __future__ import unicode_literals

import codecs
from configparser import ConfigParser
import os

DATA_DIRECTORY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))


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


def _get_versions_dict():
    """Parse the preferred versions list in data/requirements.txt into a
    dictionary for ease of use in tests"""
    path = os.path.join(DATA_DIRECTORY_PATH, 'requirements.txt')
    lines = get_file_lines(path)
    result = {}
    for line in lines:
        if '==' not in line:
            continue
        name, version = tuple(line.split('=='))
        result[name] = version
    return result

VERSIONS = _get_versions_dict()
