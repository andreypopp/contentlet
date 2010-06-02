""" Tests for contentlet.expressions."""

import unittest

from contentlet.tests import IsolatedRegistryTestCase

__all__ = ["TestProviderExpression"]


class DummyProvider(object):

    def __init__(self, content):
        self.content = content

    def __call__(self, context, request):
        return self.content


class DummyRequest(object):

    def __init__(self, registry, context=None):
        self.registry = registry
        self.context = context


class TestProviderExpression(IsolatedRegistryTestCase):

    def _registerTranslator(self, translator):
        from zope.component import getSiteManager
        from chameleon.zpt.interfaces import IExpressionTranslator
        getSiteManager().registerUtility(translator, IExpressionTranslator,
                                         name="contentprovider")

    def _registerProvider(self, provider, name, context_iface=None):
        from zope.interface import Interface
        from contentlet.interfaces import IContentProvider
        if context_iface is None:
            context_iface = Interface
        from zope.component import getSiteManager
        getSiteManager().registerAdapter(
            provider, (context_iface,), IContentProvider, name=name)

    def _createRequest(self, context=None):
        from zope.component import getSiteManager
        return DummyRequest(getSiteManager(), context=context)

    def test_it(self):
        from contentlet.expression import ProviderExpression
        self._registerTranslator(ProviderExpression())
        self._registerProvider(DummyProvider("content"), "name")
        from chameleon.zpt.template import PageTemplate
        template = PageTemplate("""\
        <div tal:replace="contentprovider:name">
          Hello World!
        </div>""", None)
        rendered = template(request=self._createRequest())
        self.assertEqual(rendered, "content")

    def test_no_provider(self):
        from contentlet.expression import ProviderExpression
        self._registerTranslator(ProviderExpression())
        from chameleon.zpt.template import PageTemplate
        template = PageTemplate("""\
        <div tal:replace="contentprovider:name">
          Hello World!
        </div>""", None)
        rendered = template(request=self._createRequest())
        self.assertEqual(rendered, "")
