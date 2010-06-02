""" Common tests and utilities."""

import unittest

__all__ = ["IsolatedRegistryTestCase"]


class IsolatedRegistryTestCase(unittest.TestCase):
    """ Test case that use isolated component registry on each test."""

    def setUp(self):
        from zope.component import getSiteManager
        from zope.component.registry import Components
        registry = Components()
        def get_registry(context=None):
            return registry
        getSiteManager.sethook(get_registry)

    def tearDown(self):
        from zope.component import getSiteManager
        getSiteManager.reset()
