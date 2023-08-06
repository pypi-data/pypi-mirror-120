#!/usr/bin/env python3
# coding: utf-8
__version__ = '0.2.3'

import os

import volkanic


class GlobalInterface(volkanic.GlobalInterface):
    package_name = 'joker.environ'
    _meta = {}

    @classmethod
    def under_joker_dir(cls, *paths):
        path = os.environ.get('JOKER_HOME', cls.under_home_dir('.joker'))
        if not cls._meta.get('joker_dir_made'):
            os.makedirs(path, int('700', 8), exist_ok=True)
            cls._meta['joker_dir_made'] = True
        return os.path.join(path, *paths)

    @classmethod
    def _get_conf_paths(cls):
        """
        Make sure this method can be called without arguments.
        Override this method in your subclasses for your specific project.
        """
        if not cls.package_name.startswith('joker.'):
            return super()._get_conf_paths()
        subpkg_name = cls.package_name[6:]
        assert subpkg_name
        return [
            cls.under_joker_dir('{}/config.json5'.format(subpkg_name)),
            '/etc/joker/{}/config.json5'.format(subpkg_name),
        ]

    _get_conf_search_paths = None


__gi = GlobalInterface()


def under_joker_dir(*paths):
    return __gi.under_joker_dir(*paths)


# deprecated
def make_joker_dir(*paths):
    return under_joker_dir(*paths)
