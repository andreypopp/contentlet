""" Tests for contentlet.provider."""

import unittest

from zope.interface import implements

from contentlet.interfaces import IContentProvider
from contentlet.provider import get_provider

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
        from repoze.bfg.registry import Registry
        self.registry = Registry()

    def _createRequest(self, context):
        return DummyRequest(self.registry, context)

    def _registerProvider(self, provider, name, context_iface=None):
        from zope.interface import Interface
        if context_iface is None:
            context_iface = Interface
        self.registry.registerAdapter(
            provider, (context_iface,), IContentProvider, name=name)

    def test_get_provider_success(self):
        self._registerProvider(DummyContentProvider("content"), "name")
        request = self._createRequest(None)
        provider = get_provider("name", request=request)
        from contentlet.interfaces import IContentProvider
        self.assertTrue(IContentProvider.providedBy(provider))
        self.assertEqual(provider(request, None), "content")

    def test_get_provider_no_provider(self):
        request = self._createRequest(None)
        self.assertRaises(LookupError, get_provider, "name", request=request)

    def test_get_provider_for_context(self):
        from zope.interface import implementedBy
        self._registerProvider(DummyContentProvider("content"), "name",
                               context_iface=implementedBy(DummyContext))
        request = self._createRequest(DummyContext())
        provider = get_provider("name", request=request)
        from contentlet.interfaces import IContentProvider
        self.assertTrue(IContentProvider.providedBy(provider))
        self.assertEqual(provider(request, None), "content")
        request = self._createRequest(None)
        self.assertRaises(LookupError, get_provider, "name", request=request)
