audit-python-package
====================
``audit-python-package`` checks the compliance of a Python source code
repository with our current packaging best practices.  It has a variety of
checks pertaining to things like:

* Versions of fundamental dependencies
* Unit test execution
* Code coverage of tests
* Supported Python version(s)
* Documentation
* Package metadata

It's implemented as a set of Python unit tests executed via pytest.  But
unlike most unit tests that are tailored to the code they're packaged with,
these ones look at the files under the directory from which they're executed.
Additional checks can be added as new test cases; doing so is usually pretty
trivial, most of the checks so far are only 1-2 lines of code each.

Currently all tests are always run, but we can start customizing this by
conditionally skipping certain test cases based on the repository's content
and/or a configuration file.

Installation
------------
The easiest way to add support for auditing a package is to add a new test
environment to its tox.ini::

    [testenv:audit]
    commands =
        pip --trusted-host pypi.safaribooks.com --disable-pip-version-check install --allow-all-external --find-links http://pypi.safaribooks.com/packages/ --allow-unverified audit-python-package --upgrade --quiet audit-python-package readme
        py.test --pyargs audit_python_package
        python setup.py check --restructuredtext --strict --metadata

This gets the latest version of the packaging checks and then runs them.  Just
run ``tox -e audit`` from the package's root directory and start fixing the
issues that cause tests to fail (and updating any checks that no longer reflect
how we want to package our code).

Skipping Individual Checks
--------------------------
If some checks don't make sense for your particular package (but do for enough
others that they're still worth enabling by default), you can specifically
disable them via pytest's ``-k`` option::

    py.test --pyargs audit_python_package -k "not test_documentation_exists and not test_sbo_sphinx_version"

Tracking Dependency Updates
---------------------------
Detailed reports on the status of pinned dependency versions compared to their
latest releases can be obtained via `requires.io <https://requires.io/>`_.
These reports include Python 3 compatibility status, changelogs between the
currently used and latest available versions, and any security issues reported
for the versions currently in use.  The site can be configured to auto-scan
GitHub and Bitbucket repositories that it can access, but we'll focus here on
their API which also supports private reports on private repositories that the
requires.io site isn't allowed to access.

First, obtain an API token for your requires.io account.  Store it in a
REQUIRES_TOKEN environment variable, for example in ``.bash_profile``::

    export REQUIRES_TOKEN=1234567890abcdef

This allows using the requires.io API from scripts in any number of repositories
without needing to store the key in multiple insecure places.

Next, add a new test environment to tox.ini::

    [testenv:requirements]
    passenv = REQUIRES_TOKEN
    commands =
        pip install --disable-pip-version-check --quiet requires.io==0.2.2
        requires.io update-repo -r my-repo-name --private
        requires.io update-branch -r my-repo-name -n `git rev-parse --abbrev-ref HEAD` requirements/*.txt
    whitelist_externals = git

You can replace ``private`` with ``public`` if creating a dependencies report
that should be visible to the general public.
