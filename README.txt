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
  A list of packages that should be tested. Defaults to the eggs of the
  [test] part, if available. Tests of these packages and all their
  dependencies will be run.

test-script
  The file system location of a `zc.recipe.testrunner` test runner, which
  needs to be configured correctly to run all tests for all specified eggs.
  Defaults to ``bin/test``.

exclude
  A list of eggs which should be excluded from the test runs. The values are
  interpreted as Python regular expressions.

groups
  A buildout section containing a mapping of group names to package names.

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


Reporting bugs or asking questions
----------------------------------

We have a shared bugtracker and help desk on Launchpad:
https://bugs.launchpad.net/collective.buildout/
