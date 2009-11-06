import os
import sys
import time

RUNNING_TESTS = '#### Running tests for %s ####'
FINISHED_TESTS = '#### Finished tests for %s ####\n'
TEST_COMMAND = '%(script)s --exit-with-status --test-path %(path)s %(arg)s -s %(package)s'


def run_test(name, script, path, arg, package):
    error = False
    print RUNNING_TESTS % name
    value = os.system(TEST_COMMAND % dict(
        script=script,
        path=path,
        arg=arg,
        package=package,
    ))
    if value > 0:
        error = True
    print FINISHED_TESTS % name
    return error


def main(args):
    testscript = os.path.abspath(args.get('testscript'))
    packages = args.get('packages')
    total_packages = len(packages)
    paths = args.get('paths')
    groups = args.get('groups')
    arg = ' '.join(sys.argv[1:])

    errors = []
    start = time.time()

    # First run grouped tests
    for group in sorted(groups):
        members = groups[group]
        for m in members:
            if m in packages:
                packages.remove(m)
        package = ' -s '.join(members)
        path = ' --test-path '.join([paths.get(p) for p in members])
        name = 'group %s' % group
        value = run_test(name, testscript, path, arg, package)
        if value:
            errors.append(name)

    # Next run tests for the remaining individual packages
    for package in packages:
        path = paths.get(package)
        value = run_test(package, testscript, path, arg, package)
        if value:
            errors.append(package)

    if len(errors):
        print "Packages with test failures:\n"
        for e in errors:
            print 'Failing tests in %s' % e
    print "\nTotal time elapsed: %.3f seconds" % (time.time()-start)
    print "\nGrand total: %d packages, %d failures\n" % (
        total_packages, len(errors)
    )

    if len(errors) > 0:
        sys.exit(1)
    sys.exit(0)
