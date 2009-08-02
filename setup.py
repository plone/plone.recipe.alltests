import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description=(
        read('README.txt')
        + '\n' +
        read('CHANGES.txt')
    )

setup(
    name = 'plone.recipe.alltests',
    version = '1.0',
    author = "Hanno Schlichting",
    author_email = "hanno@hannosch.eu",
    description = "Buildout recipe for running tests isolated at package boundaries",
    long_description=long_description,
    license = "ZPL 2.1",
    keywords = "zope2 buildout",
    url='http://pypi.python.org/pypi/plone.recipe.alltests',
    classifiers=[
      "License :: OSI Approved :: Zope Public License",
      "Framework :: Buildout",
      "Framework :: Plone",
      "Framework :: Zope2",
      "Programming Language :: Python",
      ],
    tests_require=['zope.testing'],
    packages = find_packages('src'),
    include_package_data = True,
    package_dir = {'':'src'},
    namespace_packages = ['plone', 'plone.recipe'],
    install_requires = [
        'zc.buildout',
        'setuptools',
        'zc.recipe.egg',
    ],
    zip_safe=False,
    entry_points = {
        'zc.buildout': ['default = %s:Recipe' % 'plone.recipe.alltests']
    },
    )
