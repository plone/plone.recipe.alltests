# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import os
import pkg_resources
import sys
import threading
import time

try:
    import queue
except ImportError:
    import Queue as queue

parser = argparse.ArgumentParser(
    description='testrunner running all tests in a buildout environment'
                ' grouped at once',
    version=pkg_resources.get_distribution("plone.recipe.alltests").version,
)
parser.add_argument(
    "-t", "--threads",
    dest="threads",
    type=int,
    default=1,
    help="Number of parallel threads to run tests in.",
)

parser.add_argument(
    "-g", "--groups",
    dest="groups",
    nargs='*',
    default=[],
    help="Only test given groups",
)
parser.add_argument(
    "testparameters",
    nargs="?",
    default='',
    help="Optional parameters passed to the testrunner (in quotes)",
)

RUNNING_TESTS = '#### Running tests for {0} ####'
FINISHED_TESTS = '#### Finished tests for {0} ####\n'
TEST_COMMAND = '{script} --exit-with-status --test-path {path} {arg}' +\
               ' -s {package}'


def run_test(name, script, path, arg, package):
    """runs a single test

    needs to be thread safe
    """
    print(RUNNING_TESTS.format(name))
    sys.stdout.flush()
    # todo: here it would be better to use subprocess
    value = os.system(
        TEST_COMMAND.format(
            script=script,
            path=path,
            arg=arg,
            package=package
        )
    )
    print(FINISHED_TESTS.format(name))
    sys.stdout.flush()
    return value == 0


def worker(idx, todos, errors):
    """thread queue worker

    needs to be thread safe
    ``idx``
        is the threads counter value on start
    ``todos``
        queue with tuples of name and arguments to be passed to run_test
    ``errors``
        is a list of group names withnfailed tests to be filled.

    returns always ``None`` (state is communicated via ``errors'``)
    """
    while True:
        try:
            args = todos.get_nowait()
        except queue.Empty:
            return
        ok = run_test(*args)
        if not ok:
            errors.append(args[0])


def main(config):
    #argv = sys.argv[1:]
    arguments = parser.parse_args()
    testscript = os.path.abspath(config.get('testscript'))
    packages = config.get('packages')
    total_packages = len(packages)
    paths = config.get('paths')
    groups = config.get('groups')

    errors = []
    start = time.time()

    todos = queue.Queue()

    # First run grouped tests
    for group in sorted(groups):
        if arguments.groups\
           and group not in arguments.groups:
            continue

        members = groups[group]
        for m in members:
            if m in packages:
                packages.remove(m)
        package = ' -s '.join(members)
        path = ' --test-path '.join([
            paths.get(p) for p in members
            if paths.get(p) is not None
        ])
        name = 'group %s' % group
        todos.put_nowait(
            (name, testscript, path, arguments.testparameters, package)
        )

    # Next run tests for the remaining individual packages
    for package in packages:
        if arguments.groups\
           and package not in arguments.groups:
            continue

        path = paths.get(package)
        todos.put_nowait(
            (package, testscript, path, arguments.testparameters, package)
        )

    if not todos.qsize():
        print('With given configuration there are no matching tests to run.')
        sys.exit(78)  # configuration error (see sysexits.h)

    # start the threads with the queue workers
    if arguments.threads > 1:
        # use threading
        print("Start testrunner Using {0} parallel threads".format(
            arguments.threads
        ))
        threads = []
        for idx in range(arguments.threads):
            thread = threading.Thread(
                target=worker,
                args=(idx, todos, errors)
            )
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
    else:
        # do not use threading
        print("Start testrunner in serial processing mode.")
        worker(None, todos, errors)

    if len(errors):
        print('Packages with test failures:\n')
        for error in errors:
            print('Failing tests in {0}'.format(error))
    print("\nTotal time elapsed: {0:.3f} seconds".format((time.time()-start)))
    print(
        "\nGrand total: {0:d} packages, {1:d} failures\n".format(
            total_packages,
            len(errors)
        )
    )
    if len(errors) > 0:
        sys.exit(1)
    sys.exit(0)
