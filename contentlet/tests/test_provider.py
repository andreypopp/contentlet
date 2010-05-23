""" Tests for contentlet.provider."""

import unittest

from zope.interface import implements

from contentlet.interfaces import IContentProvider
from contentlet.provider import get_provider
from contentlet.provider import query_provider

__all__ = ["TestGetProvider"]


class DummyContentProvider(object):
    implements(IContentProvider)

    def __init__(self, content):
        self.content = content

    def __call__(self, context, request):
        return self.content


class DummyRequest(object):

    def __init__(self, registry, context):
        self.registry = registry
        self.context = context


class DummyContext(object):

    pass


class TestGetProvider(unittest.TestCase):

    def setUp(self):
        from zope.component.registry import Components
        self.registry = Components()

    def _registerProvider(self, provider, name, context_iface=None):
        from zope.interface import Interface
        if context_iface is None:
            context_iface = Interface
        self.registry.registerAdapter(
            provider, (context_iface,), IContentProvider, name=name)

    def test_get_provider_success(self):
        self._registerProvider(DummyContentProvider("content"), "name")
        provider = get_provider("name", registry=self.registry)
        from contentlet.interfaces import IContentProvider
        self.assertTrue(IContentProvider.providedBy(provider))
        self.assertEqual(provider(None, None), "content")

    def test_get_provider_no_provider(self):
        self.assertRaises(LookupError, get_provider, "name",
                          registry=self.registry)

    def test_get_provider_for_context(self):
        from zope.interface import implementedBy
        self._registerProvider(DummyContentProvider("content"), "name",
                               context_iface=implementedBy(DummyContext))
        provider = get_provider("name", context=DummyContext(),
                                registry=self.registry)
        from contentlet.interfaces import IContentProvider
        self.assertTrue(IContentProvider.providedBy(provider))
        self.assertEqual(provider(None, None), "content")
        self.assertRaises(LookupError, get_provider, "name",
                          registry=self.registry)


class TestQueryProvider(unittest.TestCase):

    def setUp(self):
        from zope.component.registry import Components
        self.registry = Components()

    def _registerProvider(self, provider, name, context_iface=None):
        from zope.interface import Interface
        if context_iface is None:
            context_iface = Interface
        self.registry.registerAdapter(
            provider, (context_iface,), IContentProvider, name=name)

    def test_query_provider_success(self):
        self._registerProvider(DummyContentProvider("content"), "name")
        provider = query_provider("name", registry=self.registry)
        from contentlet.interfaces import IContentProvider
        self.assertTrue(IContentProvider.providedBy(provider))
        self.assertEqual(provider(None, None), "content")

    def test_query_provider_no_provider(self):
        provider = query_provider("name", registry=self.registry)
        self.assertEqual(provider, None)

    def test_query_provider_for_context(self):
        from zope.interface import implementedBy
        self._registerProvider(DummyContentProvider("content"), "name",
                               context_iface=implementedBy(DummyContext))
        provider = query_provider("name", context=DummyContext(),
                                registry=self.registry)
        from contentlet.interfaces import IContentProvider
        self.assertTrue(IContentProvider.providedBy(provider))
        self.assertEqual(provider(None, None), "content")
        provider = query_provider("name", registry=self.registry)
        self.assertEqual(provider, None)
