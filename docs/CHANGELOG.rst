audit-python-package Changelog
==============================

1.5.0 (2015-06-05)
------------------
* Added tests for requirements/clean_up_requirements.py and usage of it in
  git-hooks/post-merge and tox.ini
* Added tests for requirements/uninstall.txt
* Upgraded setuptools, pip, tox, and virtualenv recommended versions

1.4.2 (2015-05-29)
------------------
Added requires.io requirement (0.2.4) to setup.py.

1.4.1 (2015-05-28)
------------------
* Updated several recommended versions
* Removed setup.py from files uploaded to requires.io (the bug in their library
  that required it has been fixed)

1.4.0 (2015-05-18)
------------------
* Added upload_requirements script to easily track dependencies in requires.io

1.3.0 (2015-05-06)
------------------
* Added check for reporting of lines not covered by tests
* Switch post-merge check to recommend fetching setuptools & pip versions
  from requirements/base.txt
* Allow for pip parameters like "--trusted-host" in git-hooks/post-merge

1.2.1 (2015-04-30)
------------------
Added data/requirements.txt to packae in order to fix broken version checks

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
