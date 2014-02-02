import os
import re

from zc.buildout import easy_install
from zc.recipe.egg import Egg


EXCLUDE_PACKAGES = set((
    'distribute',
    'setuptools',
    'plone.recipe.alltests',
    'zc.buildout',
    'zc.recipe.egg',
))


class Recipe(object):

    def __init__(self, buildout, name, options):
        self.buildout, self.options, self.name = buildout, options, name
        self.egg = Egg(buildout, options['recipe'], options)

        bin_test = os.path.join(buildout['buildout']['bin-directory'], 'test')
        self.testscript = self.options.get('test-script', bin_test)

        if 'eggs' not in self.options:
            # Fallback to [test]'s eggs if available.
            if 'test' in self.buildout:
                self.options['eggs'] = self.buildout['test'].get('eggs')

        self.default_policy = self.options.get('default-policy', 'include').strip()

        self.exclude = self.options.get('exclude', '').split()
        self.exclude_groups = self.options.get('exclude-groups', '').split()
        self.include = self.options.get('include', '').split()
        self.include_groups = self.options.get('include-groups', '').split()

        options['location'] = os.path.join(
            buildout['buildout']['parts-directory'],
            self.name,
        )

    def install(self):
        options = self.options
        location = options['location']

        reqs, ws = self.egg.working_set(['plone.recipe.alltests'])

        packages = []
        paths = {}
        for dist in ws.by_key.values():
            name = dist.project_name
            packages.append(name)
            paths[name] = dist.location

        excludes = [re.compile(e) for e in self.exclude]
        includes = [re.compile(e) for e in self.include]

        filtered_packages = []
        for p in list(set(packages) - EXCLUDE_PACKAGES):
            match = False
            if self.default_policy == 'include':
                for e in excludes:
                    if e.search(p) is not None:
                        match = True
                        break
                if not match:
                    filtered_packages.append(p)
            elif self.default_policy == 'exclude':
                for i in includes:
                    if i.search(p) is not None:
                        match = True
                        break
                if match:
                    filtered_packages.append(p)
        packages = filtered_packages

        # Allow to map distribution names to different package names
        pmap = dict()
        package_map = options.get('package-map', '').strip()
        if package_map:
            pmap = self.buildout[package_map]

        for k, v in pmap.items():
            if k in packages:
                packages.remove(k)
                packages.append(v)
                paths[v] = paths[k]
                del paths[k]
        packages.sort()

        # Allow to group multiple packages into one test run
        groups = dict()
        groups_section = options.get('groups', '').strip()
        if groups_section:
            data = self.buildout[groups_section]
            for k, v in data.items():
                if self.default_policy == 'include':
                    if k in self.exclude_groups:
                        for p in v.split():
                            if p in packages:
                                packages.remove(p)
                    else:
                        groups[k] = v.split()
                elif self.default_policy == 'exclude' and k in self.include_groups:
                    groups[k] = v.split()

        easy_install.scripts(
            [(self.name, 'plone.recipe.alltests.runner', 'main')],
            ws, options['executable'], options['bin-directory'],
            arguments=dict(
                packages=packages,
                testscript=self.testscript,
                paths=paths,
                groups=groups,
                ),
            )

        return location

    def update(self):
        return self.install()
