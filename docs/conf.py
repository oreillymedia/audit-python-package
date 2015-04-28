#!/usr/bin/env python
# encoding: utf-8
"""
Sphinx configuration for documentation
"""

from sbo_sphinx.conf import *

project = 'audit-python-package'
apidoc_exclude = [
    os.path.join('docs', 'conf.py'),
    'setup.py',
    've',
]
