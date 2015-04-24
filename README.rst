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
        pip --trusted-host pypi.safaribooks.com --disable-pip-version-check install --allow-all-external --find-links http://pypi.safaribooks.com/packages/ --allow-unverified audit-python-package --upgrade audit-python-package
        py.test --pyargs audit_python_package

This gets the latest version of the packaging checks and then runs them.  Just
run ``tox -e audit`` from the package's root directory and start fixing the
issues that cause tests to fail (and updating any checks that no longer reflect
how we want to package our code).
