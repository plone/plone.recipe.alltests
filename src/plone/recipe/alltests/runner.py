import os
import sys

def main(args):
    testscript = os.path.abspath(args.get('testscript'))
    packages = args.get('packages')
    paths = args.get('paths')

    arg = ' '.join(sys.argv[1:])

    errors = []
    for p in packages:
        print '#### Running tests for %s ####' % p
        testpath = paths.get(p)
        value = os.system('%s --exit-with-status --test-path %s %s -s %s' % (testscript, testpath, arg, p))
        if value > 0:
            errors.append(p)
        print '#### Finished tests for %s ####' % p
        print

    print
    print '#### Begin test results ####'
    for e in errors:
        print 'Failing tests in %s' % e
    print '#### End test results ####'

    if len(errors) > 0:
        sys.exit(1)
    sys.exit(0)
