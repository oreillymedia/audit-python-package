audit-python-package Changelog
==============================

1.1.0 (2015-04-27)
------------------
* Added docs folder (and checks for it)
* Added git hooks (and checks for them)
* Added pytest-cov to core dependencies (to cope with --cov in addopts of
  packages being audited)
* Better check for *.pyc, *.pyd, and *.pyo files in .gitignore
* Better check for the installation of test requirements in tox's [testenv]
* Added utility functions for file content fixtures

1.0.0 (2015-04-24)
------------------
Initial release
