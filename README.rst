plone.recipe.alltests
=====================

This recipe creates a testrunner script which is suitable for running all
tests in a buildout environment at once.

At least in Zope2 there are frequently test isolation problems caused by too
much global state being used. Instead of fighting against these test isolation
problems, this recipe provides a convenient way to run all tests on a package
by package basis, provides an overall summary and exits with a combined status
code for all tests runs. The latter makes it possible to use this in a
buildbot environment.


Options
-------

The options you can set in the recipes section in your `buildout.cfg`.

eggs
  A list of packages that should be installed in the test environment.
  Defaults to the eggs of the [test] part, if available.
  By default, tests of these packages and all their dependencies will be run,
  unless you change the ``default-policy``.

test-script
  The file system location of a `zc.recipe.testrunner` test runner, which
  needs to be configured correctly to run all tests for all specified eggs.
  Defaults to ``bin/test``.

groups
  A buildout section containing a mapping of group names to package names.

default-policy
  Determines whether packages should be included in the test run or excluded,
  by default. Set to 'include' (the default) to include all packages in the
  Python environment, or 'exclude' to skip all packages except those
  explicity included with ``include`` or ``include-groups``.

exclude
  A list of packages which should be excluded from the test runs, if
  ``default-policy`` is include. The values are interpreted as Python
  regular expressions.

exclude-groups
  A list of groups which should be excluded from the test runs, if
  ``default-policy`` is include.

include
  A list of packages which should be included in the test runs, if
  ``default-policy`` is exclude.

include-groups
  A list of groups which should be included in the test runs, if
  ``default-policy`` is exclude.

package-map
  An buildout section containing a mapping of distribution names to package
  names.


Scripts
-------

This recipe create one script named after the recipe section.

All options are optional, so a minimal part looks like this::

  [test-all]
  recipe = plone.recipe.alltests

This creates a ``bin/test-all`` script that runs bin/test for all eggs (and
their dependencies) specified in the [test] part.

Run ``bin/test-all --help`` in order to see the possible options.


Issues, Contributions, Source Code
==================================

Contributors please read the document `Process for Plone core's development <http://docs.plone.org/develop/plone-coredev/index.html>`_

Sources are at the `Plone code repository hosted at Github <https://github.com/plone/plone.recipe.alltests>`_.

File bugs, ideas or other feedback at the `Issue tracker <https://github.com/plone/plone.recipe.alltests/issues>`_.

