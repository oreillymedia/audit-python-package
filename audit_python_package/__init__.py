from __future__ import unicode_literals

import codecs
from six.moves.configparser import ConfigParser
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
        return []
    with codecs.open(path, 'r', 'utf-8') as f:
        return [line.strip() for line in f.readlines()]


def get_requirement_lines(path):
    """Get the lines from a requirements file (or any other requirements file
    it includes) which contain a requirement specification."""
    lines = get_file_lines(path)
    result = []
    for line in lines:
        if line.startswith('#'):
            continue
        if line.startswith('-r') or line.startswith('--requirement'):
            base_dir = os.path.dirname(path)
            sub_path = os.path.join(base_dir, line.split()[-1])
            result.extend(get_requirement_lines(sub_path))
            continue
        if '==' not in line:
            continue
        line = line.partition(';')[0].strip()
        result.append(line)
    return result


def _get_versions_dict():
    """Parse the preferred versions list in data/requirements.txt into a
    dictionary for ease of use in tests"""
    path = os.path.join(DATA_DIRECTORY_PATH, 'requirements.txt')
    lines = get_requirement_lines(path)
    result = {}
    for line in lines:
        name, version = (part.strip() for part in line.split('=='))
        result[name] = version
    return result

VERSIONS = _get_versions_dict()
