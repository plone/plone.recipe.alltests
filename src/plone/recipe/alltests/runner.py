import ConfigParser
import os
import re
import sys
import time
import pkg_resources
from plone.recipe.alltests import EXCLUDE_PACKAGES


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


if __name__ == '__main__':
    cfg_file = sys.argv.pop(1)
    cfg = ConfigParser.ConfigParser()
    cfg.read(cfg_file)

    args = {}
    args['testscript'] = cfg.get('alltests', 'test-script',
                                 os.path.join('bin', 'zope-testrunner'))

    excludes = cfg.get('alltests', 'exclude', '').split()
    excludes = [re.compile(e) for e in excludes]
    args['packages'] = packages = []
    args['paths'] = paths = {}
    env = pkg_resources.Environment()
    for project_name in env:
        dists = env[project_name]
        for dist in dists:
            package_name = dist.project_name
            if package_name in EXCLUDE_PACKAGES:
                continue
            if any(e.match(package_name) is not None for e in excludes):
                continue
            packages.append(package_name)
            paths[package_name] = dist.location

    # Allow to group multiple packages into one test run
    args['groups'] = groups = dict()
    groups_section = cfg.get('alltests', 'groups', '').strip()
    if groups_section:
        for k, v in cfg.items(groups_section):
            groups[k] = v.split()

    main(args)
