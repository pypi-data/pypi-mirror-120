#!/usr/bin/env python3
# coding: utf-8

packages = [
    'joker.aligner',
    'joker.broker',
    'joker.cast',
    'joker.environ',
    'joker.flasky',
    'joker.geometry',
    'joker.masquerade',
    'joker.minions',
    'joker.pyoneliner',
    'joker.relational',
    'joker.scraper',
    'joker.stream',
    'joker.studio',
    'joker.textmanip',
    'joker.xopen'
]

projects = [
    'joker-aligner',
    'joker-broker',
    'joker-cast',
    'joker',
    'joker-flasky',
    'joker-geometry',
    'joker-masquerade',
    'joker-minions',
    'joker-pyoneliner',
    'joker-relational',
    'joker-scraper',
    'joker-stream',
    'joker-studio',
    'joker-textmanip',
    'joker-xopen'
]


def _get_joker_packages():
    import pkg_resources
    _packages = []
    for pkg in pkg_resources.working_set:
        pn = pkg.project_name
        if pn.startswith('joker-') or pn == 'joker':
            _packages.append(pkg)
    return _packages


def _get_joker_packages_with_pkgutil():
    import pkgutil
    import joker
    # https://stackoverflow.com/a/57873844/2925169
    return list(pkgutil.iter_modules(
        joker.__path__,
        joker.__name__ + "."
    ))


def get_joker_packages(use_pkgutil=False):
    if use_pkgutil:
        return _get_joker_packages_with_pkgutil()
    else:
        return _get_joker_packages()
