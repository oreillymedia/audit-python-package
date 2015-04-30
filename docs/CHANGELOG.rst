audit-python-package Changelog
==============================

1.2.0 (2015-04-30)
------------------
* Reformatted dependency versions mapping as a requirements.txt file that can
  be uploaded to Versioneye, etc. for comparison against the latest available
  versions
* Switched long description check from setup.cfg to setting long_description
  to the content of README.rst in setup.py (makes validation much easier)
* Check for versions of all dependencies in base.txt that we care enough about
  to list in the data/requirements.txt file of this package
* Added checks for [testenv:docs] in tox.ini
* Added check for reminder to update docs/CHANGELOG.rst

1.1.0 (2015-04-27)
------------------
* Added docs folder (and checks for it)
* Added git hooks (and checks for them)
* Added pytest-cov to core dependencies (to cope with --cov in addopts of
  packages being audited)
* Better check for \*.pyc, \*.pyd, and \*.pyo files in .gitignore
* Better check for the installation of test requirements in tox's [testenv]
* Added utility functions for file content fixtures

1.0.0 (2015-04-24)
------------------
Initial release
