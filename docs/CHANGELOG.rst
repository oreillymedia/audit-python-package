audit-python-package Changelog
==============================

1.6.6 (2015-10-01)
------------------
* Updated recommended versions of Babel, bleach, coverage, decorator, html5lib,
  path.py, pluggy, pytest, pytz, setuptools, sbo-sphinx, and sphinx_rtd_theme
* Added .cache directory to .gitignore recommendations to accommodate
  coverage 4.0

1.6.5 (2015-08-27)
------------------
* Updated recommended versions of ipython, pip, pytest-cov readme, setuptools,
  and virtualenv.
* Added tests for new dependencies of ipython 4.0.0: appnope, decorator,
  ipython-genutils, path.py, pexpect, pickleshare, simplegeneric, and traitlets

1.6.4 (2015-08-03)
------------------
Updated recommended versions of Babel, Jinja2, and pytest-cov.

1.6.3 (2015-07-16)
------------------
Updated checks to encourage usage of a ``requirements/tox.txt`` file for tox
and its dependencies, instead of keeping them in ``requirements/tests.txt``.
This makes it easier to keep dependencies current in Jenkins or Travis jobs
without constantly going back to edit the job configuration.

1.6.2 (2015-07-15)
------------------
* Check to makes sure that if setup.py's install_requires is derived from a
  requirements file, it respects any environment markers the file may contain
* Updated recommended versions of html5lib and ipython
* Upgraded requires.io package to 0.2.5
* Improved organization of requirements file checks

1.6.1 (2015-07-02)
------------------
* Updated recommended versions of pip, py, setuptools, sbo-sphinx, and
  virtualenv
* Added tox environment for flake8 checks, fixed reported issues

1.6.0 (2015-06-25)
------------------
* Added check for the presence of include_package_data=True and the absence of
  package_data in setup.py
* Updated checks for tox dependencies to reflect the fact that it now depends
  on pluggy
* Added checks for ipdb and its dependencies being in requirements/tests.txt
* Don't choke on environment markers when parsing requirements files
* Recurse through included requirements files when looking for a package
  specification in a requirements file
* Added checks to verify that cpython2.txt, pypy.txt, and cpython3.text
  requirements files are not present (environment markers in requirements
  files are a better way to handle this)
* Added check for an invalid 'Private :: Do Not Upload' classifier in setup.py
  to prevent accidental release of private packages to the public PyPI server
* Updated recommended package versions to reflect recent releases

1.5.0 (2015-06-05)
------------------
* Added tests for requirements/clean_up_requirements.py and usage of it in
  git-hooks/post-merge and tox.ini
* Added tests for requirements/uninstall.txt
* Upgraded setuptools, pip, pytest-catchlog, tox, and virtualenv recommended
  versions

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
Added data/requirements.txt to package in order to fix broken version checks

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
