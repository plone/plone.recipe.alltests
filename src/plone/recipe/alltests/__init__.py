import os
import re

from zc.buildout import easy_install
from zc.recipe.egg import Egg


EXCLUDE_PACKAGES = set((
    'setuptools',
    'plone.recipe.alltests',
    'zc.buildout',
    'zc.recipe.egg',
))


class Recipe(object):

    def __init__(self, buildout, name, options):
        self.buildout, self.options, self.name = buildout, options, name
        self.egg = Egg(buildout, options['recipe'], options)

        self.testscript = self.options.get('test-script')

        exclude = self.options.get('exclude', '')
        self.exclude = exclude.split()

        options['location'] = os.path.join(
            buildout['buildout']['parts-directory'],
            self.name,
        )

    def install(self):
        options = self.options
        location = options['location']

        reqs, ws = self.egg.working_set(['plone.recipe.alltests'])

        pmap = dict()
        package_map = options.get('package-map', '').strip()
        if package_map:
            pmap = self.buildout[package_map]

        packages = []
        for dist in ws.by_key.values():
            packages.append(dist.project_name)

        excludes = [re.compile(e) for e in self.exclude]
        packages = list(set(packages) - EXCLUDE_PACKAGES)

        filtered_packages = []
        for p in packages:
            match = False
            for e in excludes:
                if e.search(p) is not None:
                    match = True
            if not match:
                filtered_packages.append(p)
        packages = filtered_packages

        for k, v in pmap.items():
            if k in packages:
                packages.remove(k)
                packages.append(v)
        packages.sort()

        easy_install.scripts(
            [(self.name, 'plone.recipe.alltests.runner', 'main')],
            ws, options['executable'], options['bin-directory'],
            arguments=dict(
                packages=packages,
                testscript=self.testscript,
                ),
            )

        return location

    def update(self):
        return self.install()
