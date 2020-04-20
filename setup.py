import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.5.3.dev0'

setup(
    name='plone.recipe.alltests',
    version=version,
    author="Hanno Schlichting",
    author_email="hanno@hannosch.eu",
    description=("Buildout recipe for running tests isolated at package "
                 "boundaries"),
    long_description=(
        read('README.rst')
        + '\n' +
        read('CHANGES.rst')
    ),
    license="ZPL 2.1",
    keywords="zope2 buildout",
    url='https://pypi.org/project/plone.recipe.alltests',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Zope Public License",
        "Framework :: Buildout",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: Core",
        "Framework :: Zope2",
        "Framework :: Zope :: 4",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    tests_require=['zope.testing'],
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    namespace_packages=['plone', 'plone.recipe'],
    install_requires=[
        'zc.buildout',
        'setuptools',
        'zc.recipe.egg',
    ],
    zip_safe=False,
    entry_points={
        'zc.buildout': ['default = %s:Recipe' % 'plone.recipe.alltests']
    },
)
