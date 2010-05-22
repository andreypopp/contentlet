""" Tests for contentlet.configuration."""

import unittest

from zope.interface import implements

from contentlet.interfaces import IContentProvider

__all__ = ["TestConfigurator"]


class DummyContentProvider(object):
    implements(IContentProvider)

    def __init__(self, content):
        self.content = content

    def __call__(self, context, request):
        return self.content


class DummyContext(object):

    pass


class TestConfigurator(unittest.TestCase):

    def setUp(self):
        from repoze.bfg.registry import Registry
        self.registry = Registry()

    def _getProvider(self, name, context_iface=None):
        if context_iface is None:
            from zope.interface import Interface
            context_iface = Interface
        return self.registry.adapters.lookup(
            (context_iface,), IContentProvider, name=name, default=None)

    def _createConfigurator(self):
        from contentlet.configuration import Configurator
        return Configurator(self.registry)

    def test_add_content_provider_no_context(self):
        from zope.interface import implementedBy
        config = self._createConfigurator()
        config.add_content_provider(DummyContentProvider("content"),
                                    name="name")
        provider = self._getProvider("name")
        self.assertTrue(IContentProvider.providedBy(provider))
        self.assertEqual(provider(None, None), "content")
        provider = self._getProvider("name",
                                     context_iface=implementedBy(DummyContext))
        self.assertTrue(IContentProvider.providedBy(provider))
        self.assertEqual(provider(None, None), "content")

    def test_add_content_provider_for_context(self):
        from zope.interface import implementedBy
        config = self._createConfigurator()
        config.add_content_provider(DummyContentProvider("content"),
                                    name="name", context=DummyContext)
        provider = self._getProvider("name",
                                     context_iface=implementedBy(DummyContext))
        self.assertTrue(IContentProvider.providedBy(provider))
        self.assertEqual(provider(None, None), "content")
        provider = self._getProvider("name")
        self.assertEqual(provider, None)
